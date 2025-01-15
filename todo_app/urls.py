from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("new/", views.todo_create, name="create"),
    path("about/", views.about, name="about"),
    path("todos/", views.todo_list, name="todo_list")
    # path("edit/", views.edit, name="edit"),
]