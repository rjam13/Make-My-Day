from django.contrib import admin
from django.forms import inlineformset_factory
from .models import Question_Bank, Activated_Question_Bank, Question, Answer, Response

# Register your models here.
class AnswerInline(admin.TabularInline):
    model = Answer

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]

class QuestionInline(admin.TabularInline):
    model = Question

class QuestionBankAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]

admin.site.register(Activated_Question_Bank)
admin.site.register(Question_Bank, QuestionBankAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
admin.site.register(Response)
