from django.contrib import admin
from .models import UserProfile, Instructor, Student, Course
# from .models import User

# Register your models here.
# admin.register(User)
admin.site.register(UserProfile)
admin.site.register(Instructor)
admin.site.register(Student)
admin.site.register(Course)
