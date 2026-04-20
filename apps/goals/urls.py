from django.urls import path
from . import views

app_name = 'goals'

urlpatterns = [
    path('', views.goals_page, name='page'),
    path('add/', views.goal_create, name='add'),
    path('<int:pk>/edit/', views.goal_update, name='edit'),
    path('<int:pk>/delete/', views.goal_delete, name='delete'),
]