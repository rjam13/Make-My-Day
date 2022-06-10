from django.urls import path
from . import views
from register import views as registerViews

urlpatterns = [
path("home/", views.home, name="home"),
path("register/", registerViews.register, name="register"),
path("login", registerViews.login_request, name="login"),
path("", views.home, name="home"),
]
