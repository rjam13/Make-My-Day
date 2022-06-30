import django_tables2 as tables
from questions.models import Activated_Question_Bank

class ActivatedQuestionTable(tables.Table):
    class Meta:
        model = Activated_Question_Bank