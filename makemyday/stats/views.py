from django.shortcuts import render

from questions.models import Activated_Question_Bank
from stats.tables import ActivatedQuestionTable

# Create your views here.
def statistics_view(request):
    table = ActivatedQuestionTable(Activated_Question_Bank.objects.all())

    return render(request, "stats/stats.html", {"table": table})