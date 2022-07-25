from http.client import responses
from django.shortcuts import render
from main.models import Student
from questions.models import Question

from stats.helpers import calculate_student_section_score
from main.models import Course
from questions.models import Response
from questions.models import Section
from stats.tables import SectionScoreTable
from django.contrib.auth.decorators import login_required
from utils.verification import isInstructorOfCourse
from django.http import HttpResponseNotFound

@login_required
def per_section_stats_view(request, pk, id):
    if not isInstructorOfCourse(request, pk):
        return HttpResponseNotFound('<h1>You are not an instructor of this course</h1>')

    course = Course.objects.get(course_id=pk)
    section = Section.objects.get(section_id=id)

    data = []
    questions = Question.objects.filter(section=section)
    responses = Response.objects.filter(question__in=questions)
    student_id_set = set()
    for response in responses:
        student_id_set.add(response.student.student_id)
    for student_id in student_id_set:
        student = Student.objects.get(student_id=student_id)
        score = calculate_student_section_score(student, section)
        f_name = student.user_profile.user.first_name
        l_name = student.user_profile.user.last_name
        data.append({"student": f_name + " " + l_name, "score": score})

    table = (section, SectionScoreTable(data))
    return render(request, "stats/per_section_stats.html", {"course": course, "section": section, "table": table})

@login_required
def per_course_stats_view(request, pk):
    if not isInstructorOfCourse(request, pk):
        return HttpResponseNotFound('<h1>You are not an instructor of this course</h1>')
    tables = []
    course = Course.objects.get(course_id=pk)
    sections = Section.objects.filter(course=course)

    for section in sections:
        data = []
        questions = Question.objects.filter(section=section)
        responses = Response.objects.filter(question__in=questions)
        student_id_set = set()
        for response in responses:
            student_id_set.add(response.student.student_id)
        for student_id in student_id_set:
            student = Student.objects.get(student_id=student_id)
            score = calculate_student_section_score(student, section)
            f_name = student.user_profile.user.first_name
            l_name = student.user_profile.user.last_name
            data.append({"student": f_name + " " + l_name, "score": score})
        
        tables.append((section, SectionScoreTable(data)))
    

    return render(request, "stats/per_course_stats.html", {"course": course, "tables": tables})