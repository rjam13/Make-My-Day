from django.shortcuts import render
from django.http import HttpResponse
from .models import Question, Answer

# Create your views here.

def index(response, number):
    qs = Question.objects.get(number=number)
    answer = qs.answer_set.get(id=1)
    return HttpResponse("<h1>%s</h1></br><p>%s</p>" % (qs.name, str(answer.text)))
