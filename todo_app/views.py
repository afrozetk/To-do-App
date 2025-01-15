from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse
from .forms import CreateTodoForm, TeamForm
from .models import Todo, Team

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
        form = CreateTodoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('todo_list')
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
            return redirect('todo_list')
    else:
        form = CreateTodoForm(instance=todo)
    return render(request, "edit.html", {'form': form, 'todo': todo})

        


def createteam(request):
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            # Save the team and redirect to the team details page
            team = form.save()
            return redirect('teamdetails', team_id=team.id)
    else:
        form = TeamForm()
    
    return render(request, 'createteam.html', {'form': form})


  
def register(request: HttpRequest) -> HttpResponse:
  if request.method == 'POST':
      email = request.POST.get('email')
      password = request.POST.get('password')
      passwordconfirm = request.POST.get('passwordconfirm')
  return render(request, "register.html")

def edit_team(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    
    if request.method == 'POST':
        team.name = request.POST.get('teamname')
        team.description = request.POST.get('description')
        team.save()
        return redirect('teamdetails', team_id=team.id)

    return render(request, 'edit_team.html', {'team': team})


def teams_list(request):
    teams = Team.objects.all()
    return render(request, "teams.html", {'teams': teams})

def teamdetails(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    
    if request.method == 'POST':
        form = TeamForm(request.POST, instance=team)
        if form.is_valid():
            form.save()
            return redirect('teamdetails', team_id=team.id)
    else:
        form = TeamForm(instance=team)
    
    members = team.members.all()  # Assuming a related member model
    return render(request, "teamdetails.html", {'team': team, 'members': members, 'form': form})