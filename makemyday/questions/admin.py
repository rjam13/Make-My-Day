from django.contrib import admin
from .models import Question_Bank, Activated_Question_Bank, Question, Answer, Response

# Register your models here.
class AnswerInline(admin.TabularInline):
    model = Answer

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]

admin.site.register(Question_Bank)
admin.site.register(Activated_Question_Bank)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
admin.site.register(Response)
