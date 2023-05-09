from django.urls import path
from . import views

urlpatterns = [
    path('', views.rules, name='rules'),
    path('rule-list/', views.rule_list, name='rule-list'),
]
