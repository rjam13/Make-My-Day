from django.shortcuts import render
from django.http import HttpResponse
from .models import Question, Answer

# Create your views here.

def index(response, question_id):
    qs = Question.objects.get(question_id=question_id)
    # answer = qs.answer_set.get(id=1)
    return render(response, "main/question.html", {"qs": qs})

def home(response):
    return render(response, "main/home.html", {})
