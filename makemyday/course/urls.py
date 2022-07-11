from course import views as courseViews
from stats import views as statsViews
from django.urls import path, include

app_name = 'course'

urlpatterns = [
    path("create/", courseViews.course_create, name="course_create"),
    path("register/", courseViews.course_register, name="course_register"),
    path('<int:pk>/', courseViews.each_courses, name='each_courses'),
    path("<int:pk>/question-banks/", include("questions.urls", namespace="questions")),
    path("<int:pk>/statistics/", statsViews.per_course_stats_view, name='course_stats_view'),
    path('delete/<int:pk>/', courseViews.CourseDelete.as_view(), name='course_delete'),
    path('edit/<int:pk>/', courseViews.CourseEdit.as_view(), name='course_edit'),
]