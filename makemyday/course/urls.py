from course import views as courseViews

from stats import views as statsViews
from django.urls import path, include

app_name = 'course'

urlpatterns = [
    path("", include('main.urls')), 
    path("get-course/", courseViews.get_course, name='get-course'),
    path("create/", courseViews.course_create, name='course-create'),
    path("register/", courseViews.course_register, name='course-register'),
    path('<int:pk>/', courseViews.each_courses, name='each-courses'),
    path("<int:pk>/sections/", include("questions.urls", namespace='questions')),
    # path("<int:pk>/statistics/", statsViews.per_course_stats_view, name='course-stats-view'),
    path('delete/<int:pk>/', courseViews.CourseDelete.as_view(), name='course-delete'),
    path('edit/<int:pk>/', courseViews.course_edit, name='course-edit'),
]