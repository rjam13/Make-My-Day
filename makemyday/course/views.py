from email import message
from multiprocessing import AuthenticationError
from django.shortcuts import render
from .course_form import CourseForm
from django.shortcuts import redirect, get_object_or_404
from main.models import Course
from django.contrib import messages
from django.views.generic.edit import DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate
from main.models import Course

# Create your views here.
@login_required
def course_create(request):
    form = CourseForm(request.POST or None)
    if form.is_valid():
            form.save()
            messages.success(request, 'Course successfully created')
            return redirect("/")  
    return render(request, "course/course.html", {'form': form})


# @login_required
# def course_create(request):
#     instructor_id = Course.objects.get(instructors= request.POST.get('instructors'))
#     print(instructor_id)
#     form = CourseForm(request.POST or None)
#     if request.method == 'POST':
#         if form.is_valid():    
#             form.save()
#             instructor = form.cleaned_data.get('instructors')
#             instructor = authenticate(instructor= instructor)
#             if instructor is not None:
#                 messages.success(request, 'Course successfully created')
#                 return redirect("/")
#             else:
#                 messages.error(request, 'Course was not successfully created')
#                 return redirect("/course")      
#         else:
#             messages.error(request, 'Issue in form')
#             form = CourseForm()    
#     return render(request, "course/course.html", {'form': form})    
# if request.user.is_authenticated():
#         username = request.user.username

