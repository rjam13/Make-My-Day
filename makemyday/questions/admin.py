from django.contrib import admin
from .models import Section, Question, Answer, Response

# Register your models here.
class AnswerInline(admin.TabularInline):
    model = Answer

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]

class QuestionInline(admin.TabularInline):
    model = Question

class SectionAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]

admin.site.register(Section, SectionAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
admin.site.register(Response)
