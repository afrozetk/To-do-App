from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("todos/new/", views.todo_create, name="create"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("todos/<int:id>/edit/", views.todo_edit, name="edit"),
    path("todos/<int:id>/delete/", views.todo_delete, name="todo_delete"),
    path("about/", views.about, name="about"),
    path("teams/new", views.createteam, name="createteam"),
    path("register/", views.register, name="register"),
    path("teams/", views.teamdetails, name="teamdetails"),
]
