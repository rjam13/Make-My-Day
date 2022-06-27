from course import views as courseViews
from django.urls import path, include

app_name = 'course'

urlpatterns = [
    path("create/", courseViews.course_create, name="course_create"),
    path('<int:pk>/', courseViews.each_courses, name='each_courses'),
    path("<int:pk>/question-banks/", include("questions.urls", namespace="questions")),
    path('delete/<int:pk>/', courseViews.CourseDelete.as_view(), name='course_delete'),
    path('edit/<int:pk>/', courseViews.CourseEdit.as_view(), name='course_edit'),
    path("apply/<int:pk>/", courseViews.course_registration, name= "course_register"),
]