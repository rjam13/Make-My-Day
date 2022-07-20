import datetime
from django.utils import timezone
from http.client import responses
from re import A
from django.shortcuts import render
from main.models import Student, UserProfile
from .models import Question_Bank, Question, Answer, Activated_Question_Bank, Response
from django_celery_beat.models import CrontabSchedule, PeriodicTask
from django.views.generic import ListView

from django.http import JsonResponse, HttpResponse
from .form import Question_Bank_Form, Question_Form
from django.contrib import messages
from django.shortcuts import redirect
from utils.helper import retrieveStudent, is_ajax
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound
from .form import Question_Bank_Form
from django.contrib import messages
from django.shortcuts import redirect
from utils.helper import retrieveStudent, is_ajax
import json

# Create your views here.

def question_bank_view(request, pk, id):
    question_bank = Question_Bank.objects.get(question_bank_id=id)
    student = retrieveStudent(request)

    # access checks
    if not student:
        return HttpResponseNotFound('<h1>You need to be a student to answer a question bank.</h1>')
    if student and not Activated_Question_Bank.objects.filter(student=student, question_bank=question_bank):
        return HttpResponseNotFound('<h1>You are not signed up for this question bank.</h1>')

    return render(request, 'question_banks/qb.html', {'qb': question_bank})

# called injunction with question_bank_view
def qb_data_view(request, pk, id):
    question_bank = Question_Bank.objects.get(question_bank_id=id)
    student = retrieveStudent(request)

    closed_qs, open_qs, upcoming_qs = question_bank.get_questions_for_student(student)
            
    return JsonResponse({
        'closed_qs': closed_qs,
        'open_qs': open_qs,
        'upcoming_qs': upcoming_qs
    })

def activate_qb(request, pk, id):
    if is_ajax(request):
        data = request.POST
        data_ = dict(data.lists())
        data_.pop('csrfmiddlewaretoken')
        print(data_)

        question_bank = Question_Bank.objects.get(question_bank_id=id)
        student = retrieveStudent(request)
        time = data_.pop('time')[0]
        hour = int(time[:2])
        minute = int(time[3:5])
        time_ = datetime.time(hour, minute, 0)

        # checks if the student has already activated it
        if Activated_Question_Bank.objects.filter(student=student, question_bank=question_bank).first():
            return JsonResponse({
                'Error': 'Error'
            })
        else:
            Activated_Question_Bank.objects.create(student=student, question_bank=question_bank, score=0, time_to_send=time_, schedule= None)
            return HttpResponse(status=200)

def question_view(request, pk, id, qid):
    question = Question.objects.get(question_id=qid)
    question_bank = Question_Bank.objects.get(question_bank_id=id)
    student = retrieveStudent(request)

    # access checks
    if not student:
        return HttpResponseNotFound('<h1>You need to be a student to answer a question.</h1>')
    if student and not Activated_Question_Bank.objects.filter(student=student, question_bank=question_bank):
        return HttpResponseNotFound('<h1>You are not signed up for answering this question.</h1>')
    if question.openDT >= timezone.now():
        return HttpResponseNotFound('<h1>This question is not yet open.</h1>')

    return render(request, 'question/question.html', {'q': question})

# called injunction with question_view
def question_data_view(request, pk, id, qid):
    student = retrieveStudent(request)
    question = Question.objects.get(question_id=int(qid))
    studentResponse = Response.objects.filter(std=student, ques=question).first()

    if studentResponse:
        correct_answer = Answer.objects.get(question=question, isCorrect=True).ans
        if hasattr(studentResponse.ans, 'ans'):
            result = {str(question): {
                'correct_answer': correct_answer, 
                'answered': studentResponse.ans.ans, 
                'explanation': studentResponse.ans.explanation}}
        else:
            result = {str(question): {'correct_answer': correct_answer, 'answered': "Did not answer"}}
        return JsonResponse({'result': result})
    else:
        answers = {}
        for a in question.get_answers():
            answers[a.ans] = a.explanation
        return JsonResponse({
            'data': answers,
            'time_Limit': str(question.time_Limit),
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
            if a.isCorrect:
                correct_answer = a.ans
            if a_selected == a.ans:
                answer = a
        
        result = {str(question): {
            'correct_answer': correct_answer, 
            'answered': a_selected,
            'explanation': answer.explanation}}

        Response.objects.create(ques=question, ans=answer, std=student)
        
        return JsonResponse({'result': result})

def create_qb(request, pk):
    print(request.method)
    form = Question_Bank_Form()
    if request.method == "POST":
        form = Question_Bank_Form(request.POST)
        if form.is_valid():
            instance = form.save()     
            messages.success(request, 'Question Bank created successfully') 
            return redirect(f"/course/{instance.course.course_id}/")
        else:
            messages.error(request, 'Error creating Question Bank Form')    
    else:
        form = Question_Bank_Form()   
    return render(request, "question_banks/qb_create.html", {'form': form, 'pk':pk})

def create_questions(request, pk):
    print(request.method)
    form = Question_Form()
    if request.method == "POST":
        form = Question_Form(request.POST)
        if form.is_valid():
            form.save()     
            messages.success(request, 'Question created successfully') 
            pk = pk
            return redirect(f"/course/{pk}/")
        else:
            messages.error(request, 'Error creating Question')    
    else:
        form = Question_Form()   
    return render(request, "question/create_question.html", {'form': form, 'pk':pk})