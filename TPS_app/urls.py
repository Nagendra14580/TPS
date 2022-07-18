from django.contrib import admin
from django.urls import path
from TPS_app import views

urlpatterns = [
    path("login/", views.login, name="login"),
    path('teams/', views.teams_view, name="teams"),
    path('locations/', views.locations_view, name="locations"),
    path('schedules/', views.schedules_view, name="schedules"),
    path('create_user/', views.create_user, name="Create user"),
    path('change_password/', views.change_password, name="Change Password"),
    path('update_profile/', views.update_profile, name="Update Profile"),
    path('get_schedules/', views.get_schedules, name="get_schedules"),
    path('get_team_members/', views.get_team_members, name="get_team_members"),
    path('add_team_players/', views.add_team_players, name="add_team_players"),
    path('remove_team_players/', views.remove_team_players, name="remove_team_players")
]