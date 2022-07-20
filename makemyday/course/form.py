from main.models import Course, Student
from django.forms import ModelForm, TextInput
from django import forms

class ManyToManyInput(TextInput):
  def value_from_datadict(self, data, files, name):
    value = data.get(name)
    if value:
      return value.split(',')

class CourseForm(ModelForm):
    class Meta:
        model = Course

        fields = ['course_name', 'description', 'students', 'access_code', 'year', 'semester']
    students = forms.ModelMultipleChoiceField(queryset=Student.objects.all(),widget=forms.CheckboxSelectMultiple)

class InstructorForm(ModelForm):
    class Meta:
        model = Course
        fields = ['course_name', 'description', 'instructors', 'access_code', 'year', 'semester']
        widgets = {
            'instructors': ManyToManyInput()
        }
    