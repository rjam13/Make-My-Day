from django.shortcuts import render
from .form import InstructorForm, StudentForm, CourseForm
from django.shortcuts import redirect
from main.models import Course
from django.contrib import messages
from django.views.generic.edit import DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from main.models import Course, Student
from django.http import HttpResponseNotFound
from django.forms import *

# Create your views here.
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
    data = {'students': student}
    print(student)
    course = Course.objects.get(course_id= pk)
    print(course)
    form = StudentForm(instance = course, initial = data)
    # for i in range(course.students.count()):    
    #     print(course.students.all()[i]) 
    if request.method == 'POST':
        form = StudentForm(request.POST, instance = course, initial = data)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully registered for a course')
            return redirect('/course')
    context = {'form':form}
    return render(request, 'course/course_form.html', context) 


# def course_registration(request, pk):
#     # print('hi')
#     course = Course.objects.get(course_id= pk)
#     form  = CourseForm(instance = course)
#     student_id = request.user.userprofile.student_id
#     # print(student_id)
#     if request.method == 'POST':
#         form = CourseForm(request.POST, instance = course)
#         if form.is_valid():
#             print('f')
#             form.save()
#             student = form.cleaned_data.get('students')
#             if student_id == student:
#                 print('s')
#                 students = Course.objects.get(pk=pk).students.all()
#                 # students.append(student)
#                 students.set_add(student)
#                 messages.success(request, 'Successfully registered for a course')
#                 return redirect('/course')
#         else:
#             messages.error(request, 'Error registering for a course')
#             form = CourseForm()
#     context = {'form':form}
#     return render(request, 'course/course_form.html', context)





# delete a course
class CourseDelete(LoginRequiredMixin, DeleteView):
    model = Course
    template_name = 'course/course_confirm_delete.html'
    success_url = reverse_lazy('course_list')


# update a course
class CourseEdit(LoginRequiredMixin, UpdateView):
    model = Course
    form_class = StudentForm 
    template_name = 'course/course_form.html'
    success_url = reverse_lazy('course_list')




