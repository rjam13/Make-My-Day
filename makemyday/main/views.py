from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from main.models import Course, Student
from django.utils import timezone
from datetime import date, datetime
from utils.helper import retrieveStudent, retrieveInstructor

def home(request):
    if request.user.is_authenticated:
        
        questions_to_display = {}
        student = retrieveStudent(request)
        instructor = retrieveInstructor(request)

        if student:
            courses = student.retrieve_courses()
            for c in courses:
                _, current_section, _ = c.retrieve_sections()
                if current_section:
                    for q in current_section.question_set.all():
                        if q.open_datetime.date() == datetime.today().date():
                            notification = student.notification_set.get(course=c)
                            questions_to_display[q] = notification
            return render(request, "main/home.html", {
            'courses': courses, 
            'questions_to_display': questions_to_display,
            'today': date.today().strftime("%B %d, %Y")})
        elif instructor:
            courses = instructor.retrieve_courses()
            return render(request, "main/home.html", {
            'courses': courses})
        
    return render(request, "main/home.html", {})
        