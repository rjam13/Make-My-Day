import datetime
from django.utils import timezone
from http.client import responses
from re import A
from django.shortcuts import render
from main.models import Student, UserProfile
from .models import Question_Bank, Question, Answer, Activated_Question_Bank, Response
from django.views.generic import ListView
from django.http import JsonResponse, HttpResponse
from .form import Question_Bank_Form
from django.contrib import messages
from django.shortcuts import redirect
from utils.helper import retrieveStudent, is_ajax

# Create your views here.
# class QuestionBankListView(ListView):
#     model = Question_Bank # sets object_list in main_qb.html
#     template_name = 'question_banks/main_qb.html'

def question_bank_view(request, pk, id):
    question_bank = Question_Bank.objects.get(question_bank_id=id)
    return render(request, 'question_banks/qb.html', {'qb': question_bank})

# called injunction with question_bank_view
def qb_data_view(request, pk, id):
    question_bank = Question_Bank.objects.get(question_bank_id=id)
    student = retrieveStudent(request)
    closed_qs = []
    open_qs = []
    upcoming_qs = []

    for q in question_bank.get_questions():
        question_Info = {}
        question_Info['time_Limit'] = str(q.time_Limit)
        question_Info['openDT'] = str(q.openDT)
        question_Info['closeDT'] = str(q.closeDT)
        question_Info['weight'] = str(q.weight)
        question_Info['question_id'] = str(q.question_id)

        # checks whether if the student has answered this question before or not
        responseToQuestion = Response.objects.filter(ques=q, std=student).first()
        # has response has an answer (wrong or correct)
        if responseToQuestion and responseToQuestion.ans:
            answer = Answer.objects.get(answer_id=responseToQuestion.ans.answer_id)
            question_Info['answerIsCorrect'] = str(answer.isCorrect)
        # has response but no answer (response was left blank)
        elif responseToQuestion:
            question_Info['answerIsCorrect'] = "False"
        # no response
        else:
            question_Info['answerIsCorrect'] = ""
        
        if q.closeDT <= timezone.now():
            closed_qs.append({str(q): question_Info})
        elif q.openDT <= timezone.now() and q.closeDT >= timezone.now():
            open_qs.append({str(q): question_Info})
        elif q.openDT >= timezone.now():
            upcoming_qs.append({str(q): question_Info})
            
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
            Activated_Question_Bank.objects.create(student=student, question_bank=question_bank, score=0, time_to_send=time_)
            return HttpResponse(status=200)

def question_view(request, pk, id, qid):
    question = Question.objects.get(question_id=qid)
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


def retrieveStudent(request):
    user = request.user
    userProfile = UserProfile.objects.filter(user=user)[0]
    return Student.objects.filter(user_profile = userProfile)[0]

def create_qb(request, pk):
    print(request.method)
    form = Question_Bank_Form()
    if request.method == "POST":
        form = Question_Bank_Form(request.POST)
        if form.is_valid():
            form.save()     
            messages.success(request, 'Question Bank created successfully') 
            return redirect("/home")
        else:
            messages.error(request, 'Error creating Question Bank Form')    
    else:
        form = Question_Bank_Form()   
    return render(request, "question_banks/qb_create.html", {'form': form, 'pk':pk})

