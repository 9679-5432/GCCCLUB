from django.urls import path
from . import views
from . import dashboard

urlpatterns = [
    path('', views.index, name='home'),

    path('members/', views.members, name='members'),
    path('gallery/', views.gallery, name='gallery'),
    path('gallery/<int:season_id>/', views.season_gallery, name='season_gallery'),

    path('contact/', views.contact, name='contact'),
    path('registration/', views.registration, name='registration'),
    path('matches/', views.matches, name='matches'),
    path('players/', views.players, name='players'),
    path('teams/', views.teams, name='teams'),
    path('points-table/', views.points_table, name='points_table'),
    path('auction/', views.auction, name='auction'),
    path('results/', views.results, name='results'),
    path('gspl/', views.gspl, name='gspl'),
    path('notice/', views.notice, name='notice'),

    # Dashboard
    path("dashboard/", dashboard.dashboard_home, name="dashboard_home"),

    path(
        "dashboard/registrations/",
        dashboard.registration_list,
        name="registration_list",
    ),

    path(
        "dashboard/registrations/<int:id>/",
        dashboard.registration_detail,
        name="registration_detail",
    ),

    path(
        "dashboard/players/",
        dashboard.players,
        name="dashboard_players",
    ),

    path(
    "dashboard/registrations/<int:id>/approve/",
    dashboard.approve_registration,
    name="approve_registration",
),

path(
    "dashboard/registrations/<int:id>/reject/",
    dashboard.reject_registration,
    name="reject_registration",
),

path(
    "dashboard/players/<int:id>/edit/",
    dashboard.edit_player,
    name="edit_player",
),

path(
    "dashboard/players/<int:id>/delete/",
    dashboard.delete_player,
    name="delete_player",
),

path(
    "dashboard/players/export/excel/",
    dashboard.export_players_excel,
    name="export_players_excel",
),

path(
    "dashboard/players/export/pdf/",
    dashboard.export_players_pdf,
    name="export_players_pdf",
),
path(
    "dashboard/registration/open/",
    dashboard.open_registration,
    name="open_registration",
),

path(
    "dashboard/registration/close/",
    dashboard.close_registration,
    name="close_registration",
),
]