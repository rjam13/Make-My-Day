from django.urls import path
from .views import QuestionBankListView, question_bank_view, qb_data_view

app_name = 'question_banks'

urlpatterns = [
    path('', QuestionBankListView.as_view(), name='main-qb-view'),
    path('<id>/', question_bank_view, name='qb-view'),
    path('<id>/data/', qb_data_view, name='qb-data-view'),
]

