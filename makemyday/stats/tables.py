import django_tables2 as tables
from django.contrib.auth.models import User
from main.models import UserProfile

class SectionScoreTable(tables.Table):
    student = tables.Column(attrs={"td": {"style": "padding-right: 25px"}})
    score = tables.Column()