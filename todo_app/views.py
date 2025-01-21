from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm, CreateTodoForm, TeamForm, MemberForm
from django.contrib import messages
from .models import Todo, Team, TeamMember

# Define views here:

def index(request: HttpRequest) -> HttpResponse:
    return render(request, "index.html")

def about(request: HttpRequest) -> HttpResponse:
    return render(request, "about.html")
  
def dashboard(request):
  todos = Todo.objects.all()  # Fetch all ToDo items from the database
  return render(request, 'dashboard.html', {'todos': todos})


def login(request: HttpRequest) -> HttpResponse:
    return render(request, "login.html")

#used chatgpt to help me with this code:
def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("index")  # Redirect to the homepage or dashboard
            else:
                form.add_error(None, "Invalid username or password")
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def forgot_password(request):
    if request.method == "POST":
        return render(request, 'forgot_password.html', {'email': request.POST['email']})
    return render(request, 'forgot_password.html')

  
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
        
def todo_delete(request: HttpRequest, id) -> HttpResponse:
    todo = Todo.objects.get(id=id)
    if todo:
        todo.delete()
    return redirect('dashboard')

  
def createteam(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            team=form.save()
            return redirect('teamdetails', pk=team.id)
    else:
        form = TeamForm()
    return render(request, 'createteam.html', {'form': form})
        

def teamdetails(request: HttpRequest, pk: int) -> HttpResponse:
    # Get team by ID and it's associated members from the DB model:
    team = get_object_or_404(Team, pk=pk)
    members = TeamMember.objects.filter(team=team)

    if request.method == 'POST':
        # Create form model with the missing team foreign key so it validates properly.
        form = MemberForm(
            request.POST, 
            instance=TeamMember(team=team)
        )
        if form.is_valid():
            form.save()
        return redirect('teamdetails', team.pk)
    else:
        form = MemberForm()
    return render(request, 'teamdetails.html', {'team': team, 'members': members, 'form': form})

def delete_team(request, pk):
    # Get team by ID and it's associated members from the DB model:
    team = get_object_or_404(Team, pk=pk)

    if request.method == 'POST':
        team.delete()
        return redirect('createteam')
    return redirect('teamdetails', pk=pk)  


def register(request: HttpRequest) -> HttpResponse:
  if request.method == 'POST':
      email = request.POST.get('email')
      password = request.POST.get('password')
      passwordconfirm = request.POST.get('passwordconfirm')
  return render(request, "register.html")

