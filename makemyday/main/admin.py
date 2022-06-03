from django.contrib import admin
from .models import Question, Answer
# from .models import User

# Register your models here.
# admin.register(User)
admin.site.register(Question)
admin.site.register(Answer)