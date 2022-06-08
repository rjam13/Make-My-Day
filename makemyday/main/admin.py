from django.contrib import admin
from .models import UserProfile, Instructor, Student, Course, Question_Bank, Activated_Question_Bank, Question, Answer, Response
# from .models import User

# Register your models here.
# admin.register(User)
admin.site.register(UserProfile)
admin.site.register(Instructor)
admin.site.register(Student)
admin.site.register(Course)
admin.site.register(Question_Bank)
admin.site.register(Activated_Question_Bank)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Response)