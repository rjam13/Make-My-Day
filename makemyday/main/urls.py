from django.urls import path
from . import views

urlpatterns = [
path("<int:number>", views.index, name="index"),
path("home/", views.home, name="home"),
path("", views.home, name="home"),
]
