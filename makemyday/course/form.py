from dis import Instruction
from pydoc import describe
from main.models import Course, Student, Instructor
from django.forms import ModelForm, TextInput
from django import forms

class ManyToManyInput(TextInput):
  def value_from_datadict(self, data, files, name):
    value = data.get(name)
    if value:
      return value.split(',')

# class StudentForm(ModelForm):
#     class Meta:
#         model = Course
#         fields = ['course_name', 'description', 'instructors', 'students']
#         widgets = {
#             'students': ManyToManyInput()
#         }


# class CourseForm(ModelForm):
#     class Meta:
#         model = Course
#         # fields = ('course_name', 'description')
#         # fields = '__all__'
#         fields = ['course_name', 'description', "instructors", 'students']
#         # widgets = {
#         #     'students': forms.SelectMultiple,
#         # }
#     students = forms.ModelMultipleChoiceField(queryset=Student.objects.all(),widget=forms.CheckboxSelectMultiple)

    
class StudentForm(ModelForm):
    class Meta:
        model = Course
        fields = ['course_name', 'description', 'students'] 
        # widgets = {
        #     'students': ManyToManyInput()
        # }
    course_name = forms.CharField(disabled= True)
    description= forms.CharField(disabled= True)
    students = forms.ModelMultipleChoiceField(queryset=Student.objects.all(),widget=forms.CheckboxSelectMultiple)

class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = ['course_name', 'students']
        widgets = {
            'students': ManyToManyInput()
        }
    # course_name = forms.ModelMultipleChoiceField(queryset=Course.objects.all(),widget=forms.CheckboxSelectMultiple)


    

# class InstructorForm(ModelForm):
#     class Meta:
#         model = Course
#         fields = ['course_name', 'description', 'instructors']
#     instructors = forms.ModelMultipleChoiceField(queryset=Instructor.objects.all(),widget=forms.CheckboxSelectMultiple)

class InstructorForm(ModelForm):
    class Meta:
        model = Course
        fields = ['course_name', 'description', 'instructors']
        widgets = {
            'instructors': ManyToManyInput()
        }
    
# class QuestionForm(forms.Form):
#     ref = forms.ModelChoiceField()
#     def __init__(self, *args, **kwargs):
#         super(MyForm, self).__init__(*args, **kwargs)
#         self.fields['ref'].queryset = Study.objects.filter(owner=request.user)    