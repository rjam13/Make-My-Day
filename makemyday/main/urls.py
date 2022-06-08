from django.urls import path
from . import views

urlpatterns = [
path("<int:question_id>", views.index, name="index"),
path("home/", views.home, name="home"),
path("", views.home, name="home"),
]
