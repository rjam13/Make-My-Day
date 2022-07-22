import datetime
from django.utils import timezone
from django.shortcuts import render
from main.models import Course
from .models import Section, Question, Answer, Response
from django.http import JsonResponse, HttpResponse
from .form import SectionForm, QuestionForm
from django.contrib import messages
from django.shortcuts import redirect
from utils.helper import retrieveStudent, is_ajax
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound
from django.contrib import messages
from django.shortcuts import redirect
from utils.helper import retrieveStudent, retrieveInstructor, is_ajax

# Create your views here.
def section_view(request, pk, id):
    section = Section.objects.get(section_id=id)
    student = retrieveStudent(request)

    # access checks
    logged_instructor = retrieveInstructor(request)
    if not logged_instructor:
        return HttpResponseNotFound('<h1>You need to be an instructor to access this page.</h1>')
    if logged_instructor and logged_instructor.instructor_id != section.course.instructor.instructor_id:
        return HttpResponseNotFound('<h1>This is not your class.</h1>')
    if student and not Course.objects.get(course_id=pk).students.filter(student_id=student.student_id).exists():
        return HttpResponseNotFound('<h1>You are not signed up for this course.</h1>')

    return render(request, 'section/section.html', {'section': section})

# called injunction with each_courses in makemyday/course/views.py
def section_data_view(request, pk, id):
    section = Section.objects.get(section_id=id)
    student = retrieveStudent(request)

    past_questions, current_questions = section.get_questions_for_student(student)
            
    return JsonResponse({
        'past_questions': past_questions,
        'current_questions': current_questions,
    })

def question_view(request, pk, id, qid):
    question = Question.objects.get(question_id=qid)
    student = retrieveStudent(request)

    # access checks
    if not student:
        return HttpResponseNotFound('<h1>You need to be a student to answer a question.</h1>')
    if student and not Course.objects.get(course_id=pk).students.filter(student_id=student.student_id).exists():
        return HttpResponseNotFound('<h1>You are not signed up for this course.</h1>')
    if question.open_datetime >= timezone.now():
        return HttpResponseNotFound('<h1>This question is not yet open.</h1>')

    return render(request, 'question/question.html', {'q': question})

# called injunction with question_view
def question_data_view(request, pk, id, qid):
    student = retrieveStudent(request)
    question = Question.objects.get(question_id=int(qid))
    studentResponse = Response.objects.filter(student=student, question=question).first()

    if studentResponse:
        correct_answer = Answer.objects.get(question=question, is_correct=True).text
        if hasattr(studentResponse.answer, 'text'):
            result = {str(question): {
                'correct_answer': correct_answer, 
                'answered': studentResponse.answer.text, 
                'explanation': studentResponse.answer.explanation}}
        else:
            result = {str(question): {'correct_answer': correct_answer, 'answered': "Did not answer"}}
        return JsonResponse({'result': result})
    else:
        answers = {}
        for a in question.get_answers():
            answers[a.text] = a.explanation
        return JsonResponse({
            'data': answers,
        })

# called when submitting a question from website
def save_question_view(request, pk, id, qid):
    if is_ajax(request):
        question = Question.objects.get(question_id=qid)
        data = request.POST
        data_ = dict(data.lists()) # contains all the answers provided where key = question, value = answer
        data_.pop('csrfmiddlewaretoken')
        print(data_)

        # retrieves the student that answered the qb
        student = retrieveStudent(request)

        correct_answer = ""

        # find the selected answer for the question
        a_selected = str(request.POST.get(str(question)))
        if len(a_selected) == 0:
            a_selected = "Did not answer"
        answer = None

        # goes through all the answers of the question, finds the correct one and compares to selected answer
        question_answers = Answer.objects.filter(question=question)

        for a in question_answers:
            if a.is_correct:
                correct_answer = a.text
            if a_selected == a.text:
                answer = a
        
        result = {str(question): {
            'correct_answer': correct_answer, 
            'answered': a_selected,
            'explanation': answer.explanation}}

        Response.objects.create(question=question, answer=answer, student=student)
        
        return JsonResponse({'result': result})

def create_section(request, pk):
    print(request.method)
    form = SectionForm()
    if request.method == "POST":
        form = SectionForm(request.POST)
        if form.is_valid():
            instance = form.save()     
            messages.success(request, 'Section created successfully') 
            return redirect(f"/course/{instance.course.course_id}/")
        else:
            messages.error(request, 'Error creating Question Bank Form')    
    else:
        form = SectionForm()   
    return render(request, "section/section_create.html", {'form': form, 'pk':pk})

def create_question(request, pk):
    print(request.method)
    form = QuestionForm()
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()     
            messages.success(request, 'Question created successfully') 
            pk = pk
            return redirect(f"/course/{pk}/")
        else:
            messages.error(request, 'Error creating Question')    
    else:
        form = QuestionForm()   
    return render(request, "question/create_question.html", {'form': form, 'pk':pk})