from django.shortcuts import render

from main.models import Course
from questions.models import Activated_Question_Bank, Question_Bank
from stats.tables import ActivatedQuestionTable
from django.contrib.auth.decorators import login_required
from utils.verification import isInstructorOfCourse
from django.http import HttpResponseNotFound

@login_required
def per_quesion_bank_stats_view(request, pk, id):
    if not isInstructorOfCourse(request, pk):
        return HttpResponseNotFound('<h1>You are not an instructor of this course</h1>')
    question_bank = Question_Bank.objects.get(question_bank_id=id)
    activated_ques_bank = Activated_Question_Bank.objects.filter(question_bank=question_bank)
    table = ActivatedQuestionTable(activated_ques_bank)

    return render(request, "stats/per_qb_stats.html", {"table": table})

@login_required
def per_course_stats_view(request, pk):
    if not isInstructorOfCourse(request, pk):
        return HttpResponseNotFound('<h1>You are not an instructor of this course</h1>')
    tables = []
    course = Course.objects.get(course_id=pk)
    question_banks = Question_Bank.objects.filter(course=course)

    for question_bank in question_banks:
        activated_ques_banks = Activated_Question_Bank.objects.filter(question_bank=question_bank)
        tables.append((question_bank, ActivatedQuestionTable(activated_ques_banks)))
    

    return render(request, "stats/per_course_stats.html", {"tables": tables})