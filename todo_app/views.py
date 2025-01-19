from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm, CreateTodoForm, TeamForm, MemberForm
from django.contrib import messages
from .models import Todo, Team
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

# Define views here:

def index(request: HttpRequest) -> HttpResponse:
    return render(request, "index.html")

def about(request: HttpRequest) -> HttpResponse:
    return render(request, "about.html")
  
def dashboard(request):
  todos = Todo.objects.all()  # Fetch all ToDo items from the database
  return render(request, 'dashboard.html', {'todos': todos})

def login(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            # Extract data from the form
            user = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Authenticate the user
            user = authenticate(request, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Logged in successfully!")
                return redirect("index")  # Redirect to your homepage or dashboard
            else:
                messages.error(request, "Invalid email or password.")
    else:
        form = LoginForm()
    
    return render(request, "login.html", {"form": form})

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
    team = get_object_or_404(Team, pk=pk)
    members = team.name
    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            member = form.save(commit=False)
            member.team = team
            member.save()
            return redirect('teamdetails', team.pk)
    else:
        form = MemberForm()
    return render(request, 'teamdetails.html', {'team': team, 'members': members, 'form': form})

  
def register(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        # Collect form data
        email = request.POST.get('email')
        password = request.POST.get('password')
        passwordconfirm = request.POST.get('passwordconfirm')
        
        # Validate input
        if not email or not password:
            messages.error(request, "All fields are required.")
            return render(request, "register.html")

        if password != passwordconfirm:
            messages.error(request, "Passwords do not match.")
            return render(request, "register.html")
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return render(request, "register.html")
        
        # Create user
        user = User.objects.create(
            email=email,
            password=make_password(password)  # Hash the password
        )
        user.save()
        
        messages.success(request, "Account created successfully. Please log in.")
        return redirect('login')  # Redirect to login page after successful registration

    return render(request, "register.html")