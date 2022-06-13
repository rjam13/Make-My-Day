from django.shortcuts import render
from .models import Question_Bank
from django.views.generic import ListView
from django.http import JsonResponse

# Create your views here.

class QuestionBankListView(ListView):
    model = Question_Bank
    template_name = 'question_banks/main_qb.html'

def question_bank_view(request, id):
    question_bank = Question_Bank.objects.get(question_bank_id=id)
    return render(request, 'question_banks/qb.html', {'qb': question_bank})

def qb_data_view(request, id):
    question_bank = Question_Bank.objects.get(question_bank_id=id)
    questions = []
    for q in question_bank.get_questions():
        answers = []
        for a in q.get_answers():
            answers.append(a.ans)
        questions.append({str(q): answers})
    return JsonResponse({
        'data': questions
    })

# def index(response, question_id):
#     qs = Question.objects.get(question_id=question_id)
#     # answer = qs.answer_set.get(id=1)
#     return render(response, "main/question.html", {"qs": qs})