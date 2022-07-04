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
from questions.models import Question_Bank
from django.http import HttpResponse, HttpResponseNotFound
from django.forms import *
from django.shortcuts import redirect
from utils.verification import isInstructor, isStudent
from utils.helper import is_ajax, retrieveStudent

@login_required
def course_create(request):
    if not isInstructor(request):
        return HttpResponseNotFound('<h1>You are not an instructor</h1>')
    if request.method == 'POST':
        # current_user = request.user.userprofile.instructor_id
        # print(current_user)
        form = InstructorForm(request.POST)
        if form.is_valid():
                form.save()
                messages.success(request, 'Course successfully created')
                return redirect("/course")
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
    instructors = []
    for ins in list(each_one.instructors.all()):
        name = ins.user_profile.user.first_name + " " + ins.user_profile.user.last_name
        instructors.append(name)
    students = []
    for stu in list(each_one.students.all()):
        name = stu.user_profile.user.first_name + " " + stu.user_profile.user.last_name
        students.append(name)
    [closed_qbs, open_qbs, upcoming_qbs] = each_one.retrieveQuestionBanks()
    return render(request, 'course/course_info.html', 
    {'each_one': each_one, 
    'instructors': instructors, 
    'students': students,
    'open_qbs': open_qbs,
    'upcoming_qbs': upcoming_qbs})

@login_required
def course_registration(request, pk):
    student = request.user.userprofile.student_id
    instructor = request.user.userprofile.instructor_id
    print(student)
    course = Course.objects.get(course_id= pk)
    print(course)
    cc = course.students.all()
    course.students.add(student)
    print(cc)
    messages.success(request, 'Successfully registered for a course')
    return redirect(('course_list'))


# delete a course
class CourseDelete(LoginRequiredMixin, DeleteView):
    model = Course
    template_name = 'course/course_confirm_delete.html'
    success_url = reverse_lazy('course_list')


# update a course
class CourseEdit(LoginRequiredMixin, UpdateView):
    model = Course
    form_class = CourseForm 
    template_name = 'course/course_form.html'
    success_url = reverse_lazy('course_list')




