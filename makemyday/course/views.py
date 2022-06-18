from django.shortcuts import render
from .course_form import CourseForm
from django.shortcuts import redirect
from main.models import Course
from django.contrib import messages
from django.views.generic.edit import DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from main.models import Course
from django.http import HttpResponseNotFound


# Create your views here.
@login_required
def course_create(request):
    if request.user.userprofile.instructor_id == "":
        return HttpResponseNotFound('<h1>You are not an instructor</h1>')
    if request.method == 'POST':
        current_user = request.user.userprofile.instructor_id
        print(current_user)
        form = CourseForm(request.POST)
        if form.is_valid():
                form.save()
                messages.success(request, 'Course successfully created')
                return redirect("/course")
    else:
        form = CourseForm()
    return render(request, "course/course_create.html", {'form': form})

# We can possibly create a button that allows us to create a new course here in the future
@login_required
def course_list(request):
    if request.user.userprofile.instructor_id == "":
        return HttpResponseNotFound('<h1>You are not an instructor</h1>')
    courses = Course.objects.all().order_by('course_name')
    return render(request, 'course/course_list.html', {'course': courses})

@login_required
def each_courses(request, pk):
    if request.user.userprofile.instructor_id == "":
        return HttpResponseNotFound('<h1>You are not an instructor</h1>')
    each_one = Course.objects.get(pk=pk)
    return render(request, 'course/course_info.html', {'each_one': each_one})

# delete a course
class CourseDelete(LoginRequiredMixin, DeleteView):
    model = Course
    template_name = 'course/course_confirm_delete.html'
    success_url = reverse_lazy('course_list')


# update a course
class CourseEdit(LoginRequiredMixin, UpdateView):
    model = Course
    fields = '__all__'
    template_name = 'course/course_form.html'
    success_url = reverse_lazy('course_list')


