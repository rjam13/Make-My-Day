from django.urls import path
from . import views
from register import views as v

urlpatterns = [
path("home/", views.home, name="home"),
path("register/", v.register, name="register"),
path("login", v.login_request, name="login"),
path("logout", v.logout_request, name= "logout"),
path("", views.home, name="home"),
]
