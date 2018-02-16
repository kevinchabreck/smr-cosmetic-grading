from django.urls import path

from . import views

app_name = 'grading'
urlpatterns = [
  path('', views.IndexView.as_view(), name='index'),
  path('<int:test_id>/question/<int:pk>', views.QuestionView.as_view(), name='question'),
  path('<int:test_id>/question/<int:question_id>/submit', views.submit, name='submit'),
  path('<int:pk>/result/', views.ResultView.as_view(), name='result'),
]