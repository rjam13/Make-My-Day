from http.client import responses
from django.shortcuts import render
from questions.models import Question

from stats.helpers import calculate_student_section_score
from main.models import Course
from main.models import Student
from questions.models import Response
from questions.models import Section
from stats.tables import SectionScoreTable
from django.contrib.auth.decorators import login_required
from utils.verification import isInstructorOfCourse
from django.http import HttpResponseNotFound

# @login_required
# def per_section_stats_view(request, pk, id):
#     if not isInstructorOfCourse(request, pk):
#         return HttpResponseNotFound('<h1>You are not an instructor of this course</h1>')
#     section = Section.objects.get(section_id=id)
#     section_score = SectionScore.objects.filter(section=section)
#     table = SectionScoreTable(section_score)

#     return render(request, "stats/per_section_stats.html", {"table": table})

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
        print(questions)
        for question in questions:
            responses = Response.objects.filter(question=question)
            for response in responses:
                score = calculate_student_section_score(response.student, section)
                first = response.student.user_profile.user.first_name
                last = response.student.user_profile.user.last_name
                data.append({"student": first + " " + last, "score": score})
        tables.append((section, SectionScoreTable(data)))
    

    return render(request, "stats/per_course_stats.html", {"course": course, "tables": tables})