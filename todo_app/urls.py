from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("about", views.about, name="about"),
    path("createteam", views.createteam, name="createteam"),
    path("register", views.register, name="register"),
    path("teamdetails", views.teamdetails, name="teamdetails"),
]
