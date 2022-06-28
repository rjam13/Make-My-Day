import datetime
from http.client import responses
from re import A
from django.shortcuts import render
from main.models import Student, UserProfile
from .models import Question_Bank, Question, Answer, Activated_Question_Bank, Response
from django.views.generic import ListView
from django.http import JsonResponse, HttpResponse

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
    questions = []
    responses = []
    for q in question_bank.get_questions():
        question_Info = {}
        question_Info['time_Limit'] = str(q.time_Limit)
        question_Info['openDT'] = str(q.openDT)
        question_Info['closeDT'] = str(q.closeDT)
        question_Info['weight'] = str(q.weight)
        question_Info['question_id'] = str(q.question_id)

        # checks whether if the student has answered this question before or not
        student = retrieveStudent(request)
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
        
        questions.append({str(q): question_Info})
            
    return JsonResponse({
        'questions': questions,
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
    question = Question.objects.get(question_id=int(qid))
    answers = {}
    for a in question.get_answers():
        answers[a.ans] = a.explanation
    return JsonResponse({
        'data': answers,
        'time_Limit': str(question.time_Limit),
    })

# called when submitting a question from website
def save_question_view(request, pk, id, qid):
    # print(request.POST)
    if is_ajax(request):
        question = Question.objects.get(question_id=qid)
        data = request.POST
        data_ = dict(data.lists()) # contains all the answers provided where key = question, value = answer
        data_.pop('csrfmiddlewaretoken')
        print(data_)

        # retrieves the student that answered the qb
        student = retrieveStudent(request)
        
        # qb = Question_Bank.objects.get(question_bank_id=qid)

        correct_answer = None
        answeredCorrect = False
        result = {}

        # find the selected answer for the question
        a_selected = request.POST.get(str(question)) 
        answer = None

        # if question is answered
        if a_selected != "":
            # goes through all the answers of the question, finds the correct one and compares to selected answer
            question_answers = Answer.objects.filter(question=question)

            for a in question_answers:
                if a_selected == a.ans:
                    if a.isCorrect:
                        answeredCorrect = True
                        correct_answer = a.ans
                    answer = a
                else:
                    if a.isCorrect:
                        correct_answer = a.ans
            
            result = {str(question): {'correct_answer': correct_answer, 'answered': a_selected}}
        # questions is not answered
        else:
            result = {str(question): 'not answered'}

        # print(question)    
        # print(answer)
        # print(student)
        Response.objects.create(ques=question, ans=answer, std=student)

        return JsonResponse({'result': result})
        # return JsonResponse({'score': score_, 'results': results})

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def retrieveStudent(request):
    user = request.user
    userProfile = UserProfile.objects.filter(user=user)[0]
    return Student.objects.filter(user_profile = userProfile)[0]