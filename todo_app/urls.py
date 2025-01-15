from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("about", views.about, name="about"),
    path("createteams", views.createteams, name="createteams"),
    path("register", views.register, name="register")
]
