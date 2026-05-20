
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('members/', views.members, name='members'),
    path('gallery/', views.gallery, name='gallery'),
    path('contact/', views.contact, name='contact'),
    path('registration/', views.registration, name='registration'),
    path('matches/', views.matches, name='matches'),
    path('players/', views.players, name='players'),
    path('teams/', views.teams, name='teams'),
    path('points-table/', views.points_table, name='points_table'),
    path('auction/', views.auction, name='auction'),
    path('results/', views.results, name='results'),
    path('gspl/', views.gspl, name='gspl'),
    path('gallery/', views.gallery, name='gallery'),
    path('gallery/<int:season_id>/', views.season_gallery, name='season_gallery'),
    path('notice/', views.notice, name='notice'),
]