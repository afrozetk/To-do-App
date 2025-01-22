from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
    path("dashboard/", views.dashboard_view, name="dashboard_view"),
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("forgot_password/", views.forgot_password, name="forgot_password"),
    path('password-reset-success/', views.password_reset_success, name='password_reset_success'),
    path('logout/', views.logout_view, name='logout')
    path("todos/new/", views.todo_create, name="create"),
    path("todos/<int:id>/edit/", views.todo_edit, name="edit"),
    path("todos/<int:id>/setstate/", views.todo_setstate, name="todo_setstate"),
    path("todos/<int:id>/delete/", views.todo_delete, name="todo_delete"),
    path("teams/new", views.createteam, name="createteam"),
    path("teams/<int:pk>/", views.teamdetails, name="teamdetails"),
    path('teams/<int:pk>/delete/', views.delete_team, name='delete_team'),
]
