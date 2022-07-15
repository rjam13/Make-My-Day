from sqlite3 import Date
from tracemalloc import start
from django.forms import ModelForm
from .models import Question_Bank, Question
from django import forms
from bootstrap_datepicker_plus.widgets import DateTimePickerInput

class Question_Bank_Form(forms.ModelForm):
    class Meta:
        model = Question_Bank
        fields = ['course', 'assigned_students', 'topic', 'number_of_attempts', 'isRandom', 'frequency', 'start_date', 'end_date']
        widgets = {
            'start_date': DateTimePickerInput(),
            'end_date': DateTimePickerInput(),
        }

class Question_Form(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_bank', 'ques', 'order', 'time_Limit', 'openDT', 'closeDT', 'weight']
        widgets = {
            'openDT': DateTimePickerInput(),
            'closeDT': DateTimePickerInput(),
        }