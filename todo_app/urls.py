from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path('logout/', views.logout_view, name='logout'),
    path("todos/new/", views.todo_create, name="create"),
    path("todos/<int:id>/edit/", views.todo_edit, name="edit"),
    path("todos/<int:id>/setstate/", views.todo_setstate, name="todo_setstate"),
    path("todos/<int:id>/delete/", views.todo_delete, name="todo_delete"),
    path("teams/", views.teams, name="teams"),
    path("teams/new", views.createteam, name="createteam"),
    path("teams/<int:pk>/", views.teamdetails, name="teamdetails"),
    path('teams/<int:pk>/delete/', views.delete_team, name='delete_team'),
    path("forgot_password/", views.forgot_password, name="forgot_password"),
    path("password-reset/", auth_views.PasswordResetView.as_view(), name="password_reset"),
    path("password-reset/done/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path("password-reset-sent/", views.password_reset_sent, name="password_reset_sent"),

]
