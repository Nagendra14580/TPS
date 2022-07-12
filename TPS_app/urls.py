from django.contrib import admin
from django.urls import path
from TPS_app import views

urlpatterns = [
    path('teams/', views.teams_view),
    path('players/', views.players_view),
    path('locations/', views.locations_view),
    path('schedules/', views.schedules_view),
    path('get_schedules/', views.get_schedules),
    path('get_team_members/', views.get_team_members),
]