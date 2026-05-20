from django.urls import path
from . import views

urlpatterns = [
    path('', views.gspl_home, name='gspl_home'),
    path('teams/', views.teams, name='teams'),
    path('matches/', views.matches, name='matches'),
]