from django.urls import path
from .views import section_view, section_data_view, question_view, save_question_view, question_data_view, create_section, create_question
from stats import views as statsViews
from questions import views as questionViews

app_name = 'questions'

urlpatterns = [
    path('<int:id>/', section_view, name='section-view'),
    path('<int:id>/data/', section_data_view, name='section-data-view'),
    path('<int:id>/<int:qid>/', question_view, name='question-view'),
    path('<int:id>/<int:qid>/data/', question_data_view, name='question-data-view'),
    path('<int:id>/<int:qid>/save/', save_question_view, name='save-question-view'),
    path("<int:id>/statistics/", statsViews.per_section_stats_view, name='section-stats-view'),
    path("create-qb", create_section, name='create-section'),
    path("create-question", create_question, name='create-question'),
]

