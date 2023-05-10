from django.urls import path
from . import views

urlpatterns = [
    path('', views.RulesView.as_view(), name='rules'),
    path('rule-list/', views.RuleListView.as_view(), name='rule-list'),
    path('rulecreate/', views.CreateRuleView.as_view(), name='rule-create'),
    path('ruleupdate/<int:pk>', views.UpdateRuleView.as_view(), name='rule-update'),
    path('ruledelete/<int:pk>', views.DeleteRuleView.as_view(), name='rule-delete'),
]
