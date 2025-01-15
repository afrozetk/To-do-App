from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("todos/new/", views.todo_create, name="create"),
    path("todos/", views.todo_list, name="todo_list"),
    path("todos/<int:id>/edit/", views.todo_edit, name="edit"),
    path("about/", views.about, name="about"),
    path("teams/new", views.createteam, name="createteam"),
    path("register/", views.register, name="register"),
    # path("teams/", views.teamdetails, name="teamdetails"),
    # new paths
    path('teams/', views.teams_list, name='teams'),
    path('teams/<int:team_id>/edit/', views.edit_team, name='edit_team'),
    path('teams/<int:team_id>/', views.teamdetails, name='teamdetails'),
    
]


