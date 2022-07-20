from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from main.models import Course, Student
from questions.models import Activated_Question_Bank, Question_Bank
from django.utils import timezone
from datetime import date
from utils.helper import retrieveStudent, retrieveInstructor

def home(request):
    if request.user.is_authenticated:
        
        # aqbs = activated question banks
        closed_aqbs = []
        open_aqbs = []
        upcoming_aqbs = []
        courses_ = []
        student = retrieveStudent(request)
        instructor = retrieveInstructor(request)

        if student:
            closed_aqbs, open_aqbs, upcoming_aqbs = student.retrieveActivatedQuestionBanks()

            for obj in open_aqbs:
                obj.computeScore()

            courses = Course.objects.order_by('course_name')
            for cour in courses:
                # if you want to display all courses, comment the line of code below
                if student in cour.students.all():
                    instructors = []
                    for ins in list(cour.instructors.all()):
                        name = ins.user_profile.user.first_name + " " + ins.user_profile.user.last_name
                        instructors.append(name)
                    courses_.append({"course_name": str(cour), 
                    "course_id": str(cour.course_id),
                    "instructors": instructors})
        elif instructor:
            courses = Course.objects.order_by('course_name')
            for cour in courses:
                # if you want to display all courses, comment the line of code below
                if instructor in cour.instructors.all():
                    instructors = []
                    for ins in list(cour.instructors.all()):
                        name = ins.user_profile.user.first_name + " " + ins.user_profile.user.last_name
                        instructors.append(name)
                    courses_.append({"course_name": str(cour), 
                    "course_id": str(cour.course_id),
                    "instructors": instructors})
        
        return render(request, "main/home.html", {
            'courses': courses_, 
            'closed_aqbs': closed_aqbs,
            'open_aqbs': open_aqbs,
            'upcoming_aqbs': upcoming_aqbs,
            'today': date.today().strftime("%B %d, %Y")})
    return render(request, "main/home.html", {})