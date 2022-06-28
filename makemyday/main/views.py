from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from main.models import Course, Student
from questions.models import Activated_Question_Bank, Question_Bank

# Create your views here.
# def home(response):
#     return render(response, "main/home.html", {})

def home(request):
    if request.user.is_authenticated:
        
        activated_qbs = []
        # qbs = []
        # in case superuser is login, this if statement should stop the website from throwing an error
        if hasattr(request.user, "userprofile"):
            student = Student.objects.get(student_id=request.user.userprofile.student_id)
            activated_qbs = Activated_Question_Bank.objects.filter(student=student)
            # qbs = Question_Bank.objects.filter(assigned_students__in = [student])

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

        # return render(request, "main/home.html", {'courses': courses_, 'activated_qb': activated_qbs, 'qbs': qbs})
        return render(request, "main/home.html", {'courses': courses_, 'activated_qb': activated_qbs})
    return render(request, "main/home.html", {})
    # return render(request, 'course/course_list.html', {'course': courses})