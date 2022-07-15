import django_tables2 as tables
from django.contrib.auth.models import User
from main.models import UserProfile

class ActivatedQuestionTable(tables.Table):
    student = tables.Column(verbose_name="Student", attrs={"td": {"style": "padding-right: 25px"}})
    score = tables.Column()

    def render_student(self, value):
        userObject = UserProfile.objects.get(student_id=value).user
        return "{} {}".format(userObject.first_name, userObject.last_name)