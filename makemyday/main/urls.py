from django.urls import path
from . import views
from register import views as registerViews

urlpatterns = [
    path("home/", views.home, name="home"),
    path("", views.home, name="home"),
]
