from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
    path("forgot_password/", views.forgot_password, name="forgot_password"),
    path("todos/new/", views.todo_create, name="create"),
    path("todos/<int:id>/edit/", views.todo_edit, name="edit"),
    path("todos/<int:id>/setstate/", views.todo_setstate, name="todo_setstate"),
    path("todos/<int:id>/delete/", views.todo_delete, name="todo_delete"),
    path("teams/new", views.createteam, name="createteam"),
    path("teams/<int:pk>/", views.teamdetails, name="teamdetails"),
]
