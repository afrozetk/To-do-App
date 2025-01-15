from django.shortcuts import render, redirect,  get_object_or_404, redirect
from django.http import HttpRequest, HttpResponse
from .forms import CreateForm
from .models import Todo

# Define views here:

def index(request: HttpRequest) -> HttpResponse:
    return render(request, "index.html")

def about(request: HttpRequest) -> HttpResponse:
    return render(request, "about.html")

def todo_list(request):
    todos = Todo.objects.all()  # Fetch all ToDo items from the database
    return render(request, 'todo_list.html', {'todos': todos})

def todo_create(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = CreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('todo_list')
        else:
            print(form.errors)
    else:
        form = CreateForm()  
    return render(request, 'create.html', {'form': form})


def todo_edit(request, id):
    todo=get_object_or_404(Todo, id=id)
    if request.method == 'POST':
        form = CreateForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            return redirect('todo_list')
    else:
        form = CreateForm(instance=todo)
        return render(request, "edit.html", {'form': form, 'todo': todo})

        