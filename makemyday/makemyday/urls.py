"""makemyday URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from atexit import register
from django.contrib import admin
from django.urls import path, include
from register import views as registerViews
from questions import views as questionViews

urlpatterns = [
    path("admin/", admin.site.urls),
    path("<int:question_id>", questionViews.index, name="index"),
    path("register/", registerViews.register, name="register"),
    path("login", registerViews.login_request, name="login"),
    path("logout", registerViews.logout_request, name= "logout"), 
    path("", include("main.urls")),
]
