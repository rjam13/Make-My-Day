from main.models import Course
from django.forms import *

class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = ('course_id', 'course_name', 'description')
        # widgets = {
        #     'instructors': TextInput(),
        # }
    
