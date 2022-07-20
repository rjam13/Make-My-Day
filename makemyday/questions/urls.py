from django.urls import path
from .views import question_bank_view, qb_data_view, question_view, save_question_view, question_data_view, activate_qb
from stats import views as statsViews
from questions import views as questionViews

app_name = 'questions'

urlpatterns = [
    # path('', QuestionBankListView.as_view(), name='main-qb-view'),
    path('<int:id>/', question_bank_view, name='qb-view'),
    path('<int:id>/activate-qb/', activate_qb, name='qb-activate'),
    path('<int:id>/data/', qb_data_view, name='qb-data-view'),
    path('<int:id>/<int:qid>/', question_view, name='ques-view'),
    path('<int:id>/<int:qid>/data/', question_data_view, name='ques-data-view'),
    path('<int:id>/<int:qid>/save/', save_question_view, name='save-ques-view'),
    path("<int:id>/statistics/", statsViews.per_quesion_bank_stats_view, name='qb_stats_view'),
    path("create-qb", questionViews.create_qb, name='create_qb'),
    path("create-question", questionViews.create_questions, name='create_ques'),
]

