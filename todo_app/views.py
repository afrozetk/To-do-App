from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse
from .forms import CreateTodoForm
from .models import Todo

# Define views here:

def index(request: HttpRequest) -> HttpResponse:
    return render(request, "index.html")

def about(request: HttpRequest) -> HttpResponse:
    return render(request, "about.html")

  
def dashboard(request):
    todos = Todo.objects.all()  # Fetch all ToDo items from the database
    return render(request, 'dashboard.html', {'todos': todos})

def todo_create(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = CreateTodoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
        else:
            print(form.errors)
    else:
        form = CreateTodoForm()  
    return render(request, 'create.html', {'form': form})

def todo_edit(request, id):
    todo=get_object_or_404(Todo, id=id)
    if request.method == 'POST':
        form = CreateTodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = CreateTodoForm(instance=todo)
    return render(request, "edit.html", {'form': form, 'todo': todo})
        
  
def createteam(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        teamname = request.POST.get('teamname')
        description = request.POST.get('description')
        return redirect('teamdetails')
    return render(request, "createteam.html")
  
def teamdetails(request: HttpRequest) -> HttpResponse:
    return render(request, "teamdetails.html")

  
def register(request: HttpRequest) -> HttpResponse:
  if request.method == 'POST':
      email = request.POST.get('email')
      password = request.POST.get('password')
      passwordconfirm = request.POST.get('passwordconfirm')
  return render(request, "register.html")