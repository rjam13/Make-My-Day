
from .models import Section, Question
from django import forms
from bootstrap_datepicker_plus.widgets import DateTimePickerInput

class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ['course', 'topic', 'frequency', 'start_date', 'end_date']
        widgets = {
            'start_date': DateTimePickerInput(),
            'end_date': DateTimePickerInput(),
        }

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['section', 'text', 'order', 'open_datetime']
        widgets = {
            'open_datetime': DateTimePickerInput(),
        }