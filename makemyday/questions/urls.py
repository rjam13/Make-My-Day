from django.urls import path
from .views import QuestionBankListView, question_bank_view, qb_data_view, question_view, save_question_view, question_data_view

app_name = 'questions'

urlpatterns = [
    path('', QuestionBankListView.as_view(), name='main-qb-view'),
    path('<id>/', question_bank_view, name='qb-view'),
    path('<id>/data/', qb_data_view, name='qb-data-view'),
    path('<id>/<qid>/', question_view, name='ques-view'),
    path('<id>/<qid>/data/', question_data_view, name='ques-data-view'),
    path('<id>/<qid>/save/', save_question_view, name='save-ques-view'),
]

