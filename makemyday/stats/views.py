# from django.shortcuts import render

# from main.models import Course
# from questions.models import Section
# from stats.tables import SectionScoreTable
# from django.contrib.auth.decorators import login_required
# from utils.verification import isInstructorOfCourse
# from django.http import HttpResponseNotFound

# @login_required
# def per_section_stats_view(request, pk, id):
#     if not isInstructorOfCourse(request, pk):
#         return HttpResponseNotFound('<h1>You are not an instructor of this course</h1>')
#     section = Section.objects.get(section_id=id)
#     section_score = SectionScore.objects.filter(section=section)
#     table = SectionScoreTable(section_score)

#     return render(request, "stats/per_section_stats.html", {"table": table})

# @login_required
# def per_course_stats_view(request, pk):
#     if not isInstructorOfCourse(request, pk):
#         return HttpResponseNotFound('<h1>You are not an instructor of this course</h1>')
#     tables = []
#     course = Course.objects.get(course_id=pk)
#     sections = Section.objects.filter(course=course)

#     for s in sections:
#         section_score = SectionScore.objects.filter(section=s)
#         tables.append((s, SectionScoreTable(section_score)))
    

    # return render(request, "stats/per_course_stats.html", {"tables": tables})