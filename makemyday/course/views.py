import string
from django.shortcuts import render, redirect
from .form import InstructorForm, CourseForm
from main.models import Course, Notification
from questions.models import Section
from django.contrib import messages
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound
from django.forms import *
from utils.verification import isInstructor
from django.shortcuts import render
from utils.helper import is_ajax, retrieveStudent, retrieveInstructor
import datetime

def get_course(request):
    if is_ajax(request) and request.method == "GET":
        access_code = request.GET.get("access_code", None)
        try:
            course = Course.objects.get(access_code=access_code)
            instructor_name = f"{course.instructor.user_profile.user.last_name}, {course.instructor.user_profile.user.first_name} "

            return JsonResponse({
                'error': False,
                'instructor': instructor_name,
                'course_id': str(course.course_id),
                'name': str(course.name),
                'description': str(course.description),
                'year': str(course.year),
                'semester': str(course.semester),
            })
        except:
            return JsonResponse({
                'error': True
            })

@login_required
def course_create(request):
    if not isInstructor(request):
        return HttpResponseNotFound('<h1>You are not an instructor</h1>')
    instructor = retrieveInstructor(request)
    intructor_id = instructor.instructor_id
    print(intructor_id)    
    if request.method == 'POST':
        form = InstructorForm(request.POST)
        if form.is_valid():
                form.save()
                messages.success(request, 'Course successfully created')
                return redirect("/")
    else:
        form = InstructorForm()
    return render(request, "course/course_create.html", {'form': form})

@login_required
def course_register(request):
    if is_ajax(request):
        data = request.POST
        data_ = dict(data.lists())
        data_.pop('csrfmiddlewaretoken')
        
        student = retrieveStudent(request)

        course_id = data_.pop('course_id')[0]
        course = Course.objects.get(course_id=course_id)

        time = data_.pop('time')[0]
        hour = int(time[:2])
        minute = int(time[3:5])
        time_ = datetime.time(hour, minute, 0)

        # checks if the student has already activated it
        if Notification.objects.filter(student=student, course=course).first():
            return HttpResponse("You are already signed up for this course.")
        else:
            Notification.objects.create(student=student, course=course, time_to_send=time_, schedule= None)
            return HttpResponse("Code is valid")

@login_required
def course_unenroll(request):
    pass

@login_required
def change_reminder(request):
    pass
        
@login_required
def each_courses(request, pk):
    each_one = Course.objects.get(pk=pk)
    student = retrieveStudent(request)
    closed_sections, open_section, upcoming_sections = each_one.retrieve_sections()
    course_instructor = f"{each_one.instructor.user_profile.user.last_name}, {each_one.instructor.user_profile.user.first_name} "
    students = list(each_one.students.all())
    students_ = []
    past_questions = []
    
    # access checks
    logged_instructor = retrieveInstructor(request)
    if logged_instructor and logged_instructor.instructor_id != each_one.instructor.instructor_id:
        return HttpResponseNotFound('<h1>This is not your class.</h1>')
    if student and not student in students:
        return HttpResponseNotFound('<h1>You are not signed up for this class.</h1>')

    if logged_instructor:
        notification = None
    else:    
        notification = Notification.objects.get(course=each_one, student=student)
    for stu in students:
        name = stu.user_profile.user.first_name + " " + stu.user_profile.user.last_name
        students_.append(name)
    return render(request, 'course/course_info.html', 
    {'each_one': each_one, 
    'notification': notification,
    'instructor': course_instructor, 
    'students': students_,
    'closed_sections': closed_sections,
    'open_section': open_section,
    'upcoming_sections': upcoming_sections,
    })


# delete a course
class CourseDelete(LoginRequiredMixin, DeleteView):
    model = Course
    template_name = 'course/course_confirm_delete.html'
    success_url = reverse_lazy("main:home")

@login_required
def course_edit(request, pk):
    course = Course.objects.get(course_id= pk)
    form = CourseForm(instance = course)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance= course)
        if form.is_valid:
            form.save()
            messages.success(request, "You successfully updated the course")
            return redirect(f"/course/{pk}/")

    context = {'form': form}    
    return render(request, 'course/course_form.html', context)
