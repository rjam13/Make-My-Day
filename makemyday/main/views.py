from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from main.models import Course, Student
from questions.models import Activated_Question_Bank, Question_Bank
from django.utils import timezone

# Create your views here.
# def home(response):
#     return render(response, "main/home.html", {})

def home(request):
    if request.user.is_authenticated:
        
        # aqbs = activated question banks
        closed_aqbs = []
        open_aqbs = []
        upcoming_aqbs = []
        # in case superuser is login, this if statement should stop the website from throwing an error
        if hasattr(request.user, "userprofile"):
            student = Student.objects.get(student_id=request.user.userprofile.student_id)
            closed_aqbs, open_aqbs, upcoming_aqbs = student.retrieveActivatedQuestionBanks()

        for obj in open_aqbs:
            obj.computeScore()

        courses = Course.objects.all().order_by('course_name')
        courses_ = []
        for cour in courses:
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
            'upcoming_aqbs': upcoming_aqbs})
    return render(request, "main/home.html", {})