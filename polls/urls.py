from django.urls import path
from . import views

app_name = 'polls'
urlpatterns = [
    path('django/polls/', views.IndexView.as_view(), name='index'),
    path('django/polls/<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('django/polls/<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('django/polls/<int:question_id>/vote/', views.vote, name='vote'),
]
