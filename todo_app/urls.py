from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
    path("teams/", views.team_details_page, name="teams"),  
    path("login/", views.login, name="login"),

]
# from django.contrib import admin
# from django.urls import path
# from . import views 

# urlpatterns = [
#     path('admin/', admin.site.urls),  # Admin panel
#     path('', views.landing_page, name='landing_page'),  # Landing page
#     path('about/', views.about_page, name='about_page'),  # About page
#     path('register/', views.register_page, name='register_page'),  # Registration page
#     path('login/', views.login_page, name='login_page'),  # Login page
#     path('dashboard/', views.dashboard_page, name='dashboard_page'),  # Dashboard page
#     path('todos/new/', views.create_todo_page, name='create_todo_page'),  # Create ToDo page
#     path('todos/<int:id>/edit/', views.edit_todo_page, name='edit_todo_page'),  # Edit ToDo page
#     path('teams/<int:id>/', views.team_details_page, name='team_details_page'),  # Team Details page
#     path('teams/new/', views.create_team_page, name='create_team_page'),  # Create Team page
# ]
