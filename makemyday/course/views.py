from django.shortcuts import render
from .form import InstructorForm, CourseForm
from django.shortcuts import redirect
from main.models import Course
from django.contrib import messages
from django.views.generic.edit import DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from main.models import Course
from django.http import HttpResponse, HttpResponseNotFound
from django.forms import *
from django.shortcuts import redirect
from utils.verification import isInstructor, isStudent
from utils.helper import is_ajax, retrieveStudent
from django.shortcuts import render, get_object_or_404
from utils.helper import is_ajax, retrieveStudent, retrieveInstructor

@login_required
def course_create(request):
    if not isInstructor(request):
        return HttpResponseNotFound('<h1>You are not an instructor</h1>')
    current_user = request.user.userprofile.instructor_id
    print(current_user)    
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
        code = data_.pop('code')[0]
        try:
            course = Course.objects.get(access_code=code)
            course.students.add(retrieveStudent(request))
            return HttpResponse("Code is valid")
        except:
            return HttpResponse("Code is not valid")

@login_required
def each_courses(request, pk):
    each_one = Course.objects.get(pk=pk)
    instructors = list(each_one.instructors.all())
    students = list(each_one.students.all())
    instructors_ = []
    students_ = []

    if retrieveInstructor(request) and not retrieveInstructor(request) in instructors:
        return HttpResponseNotFound('<h1>This is not your class.</h1>')
    if retrieveStudent(request) and not retrieveStudent(request) in students:
        return HttpResponseNotFound('<h1>You are not signed up for this class.</h1>')

    for ins in instructors:
        name = ins.user_profile.user.first_name + " " + ins.user_profile.user.last_name
        instructors_.append(name)
    for stu in students:
        name = stu.user_profile.user.first_name + " " + stu.user_profile.user.last_name
        students_.append(name)
    [closed_qbs, open_qbs, upcoming_qbs] = each_one.retrieveQuestionBanks()
    return render(request, 'course/course_info.html', 
    {'each_one': each_one, 
    'instructors': instructors_, 
    'students': students_,
    'open_qbs': open_qbs,
    'upcoming_qbs': upcoming_qbs})


# delete a course
class CourseDelete(LoginRequiredMixin, DeleteView):
    model = Course
    template_name = 'course/course_confirm_delete.html'
    success_url = reverse_lazy("main:home")

@login_required
def course_edit(request, pk):
    course_id = Course.objects.get(course_id= pk)
    form = CourseForm(instance = course_id)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance= course_id)
        if form.is_valid:
            form.save()
            messages.success(request, "You successfully updated the course")
            return redirect(f"/course/{pk}/")

    context = {'form': form}    
    return render(request, 'course/course_form.html', context)


# update a course
# class CourseEdit(LoginRequiredMixin, UpdateView):
#     model = Course
#     form_class = CourseForm 
#     template_name = 'course/course_form.html'
#     success_url = reverse_lazy("main:home")



# @login_required
# def course_registration(request, pk):
#     student = request.user.userprofile.student_id
#     instructor = request.user.userprofile.instructor_id
#     print(student)
#     course = Course.objects.get(course_id= pk)
#     print(course)
#     cc = course.students.all()
#     course.students.add(student)
#     print(cc)
#     messages.success(request, 'Successfully registered for a course')
#     return redirect(('course_list'))