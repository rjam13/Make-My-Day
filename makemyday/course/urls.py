from course import views as courseViews
from django.urls import path, include


urlpatterns = [
    path("", courseViews.course_list, name="course_list"),
    path("create", courseViews.course_create, name="course_create"),
    path('<int:pk>', courseViews.each_courses, name='each_courses'),
    path('delete/<int:pk>', courseViews.CourseDelete.as_view(), name='course_delete'),
    path('edit/<int:pk>', courseViews.CourseEdit.as_view(), name='course_edit'),
    path("apply/<int:pk>", courseViews.course_registration, name= "course_register"),
]