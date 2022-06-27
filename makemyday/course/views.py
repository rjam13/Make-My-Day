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
from django.http import HttpResponseNotFound
from django.forms import *
from django.shortcuts import redirect


@login_required
def course_create(request):
    print(request.user.userprofile.instructor_id)
    if request.user.userprofile.instructor_id == "":
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
def course_list(request):
    courses = Course.objects.all().order_by('course_name')
    return render(request, 'course/course_list.html', {'course': courses})

@login_required
def each_courses(request, pk):
    each_one = Course.objects.get(pk=pk)
    instructors = []
    for ins in list(each_one.instructors.all()):
        instructors.append(str(ins))
    students = []
    for stu in list(each_one.students.all()):
        students.append(str(stu))
    return render(request, 'course/course_info.html', {'each_one': each_one, 'instructors': instructors, 'students': students})

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




