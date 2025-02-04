import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse
from django.contrib.auth import authenticate, logout, login as auth_login
from .forms import LoginForm, ResetPasswordForm, CreateTodoForm, TeamForm, MemberForm
from django.contrib import messages
from .models import Todo, Team, TeamMember
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

# Set up logging
logger = logging.getLogger(__name__)

# Define views here:

def index(request: HttpRequest) -> HttpResponse:
    return render(request, "index.html")

def about(request: HttpRequest) -> HttpResponse:
    return render(request, "about.html")

@login_required()
def dashboard(request: HttpRequest) -> HttpResponse:
    """Displays the to-do list with category and team filters."""
    
    # Fetch filters from request
    category_filter = request.GET.get('category', '').strip()
    team_filter = request.GET.get('team', '').strip()

    # Log filter values
    logger.info(f"Selected Category: {category_filter}")
    logger.info(f"Selected Team: {team_filter}")

    # Fetch user's personal ToDo items
    todos = Todo.objects.filter(user=request.user)

    # Get teams the user is part of and include tasks assigned to those teams
    users_teams = TeamMember.objects.filter(user=request.user)
    todos = todos.union(*[
        Todo.objects.filter(team=user_member.team).exclude(user=request.user) 
        for user_member in users_teams
    ])

    # Apply Category filter if selected
    if category_filter:
        todos = todos.filter(category__iexact=category_filter)  # Case-insensitive match

    # Apply Team filter if selected
    if team_filter:
        todos = todos.filter(team__name__iexact=team_filter)  # Case-insensitive match

    # Log final filtered results
    logger.info(f"Filtered ToDos Count: {todos.count()}")

    # Get unique categories and teams for dropdown filters
    categories = Todo.objects.filter(user=request.user).values_list('category', flat=True).distinct()
    teams = Team.objects.filter(teammember__user=request.user).values_list('name', flat=True).distinct()

    return render(request, 'dashboard.html', {
        'todos': todos,
        'categories': categories,
        'teams': teams,
        'selected_category': category_filter,
        'selected_team': team_filter
    })

@login_required()
def todo_create(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = CreateTodoForm(request.POST, instance=Todo(user=request.user))
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = CreateTodoForm()  
    return render(request, 'create.html', {'form': form})

@login_required()
def todo_edit(request, id):
    todo = get_object_or_404(Todo, id=id)
    if request.method == 'POST':
        form = CreateTodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = CreateTodoForm(instance=todo)
    return render(request, "edit.html", {'form': form, 'todo': todo})

@login_required()
def todo_setstate(request: HttpRequest, id) -> HttpResponse:
    if request.method == 'POST' and request.POST.get("state"):
        todo = get_object_or_404(Todo, id=id)
        todo.state = request.POST.get("state")
        todo.save()
    return redirect('dashboard')

@login_required()
def todo_delete(request: HttpRequest, id) -> HttpResponse:
    todo = get_object_or_404(Todo, id=id)
    if todo:
        todo.delete()
    return redirect('dashboard')

@login_required()
def teams(request: HttpRequest) -> HttpResponse:
    owned_teams = Team.objects.filter(owner=request.user)

    if not owned_teams:
        form = TeamForm()
        return render(request, 'createteam.html', {'form': form})
    
    return redirect('teamdetails', pk=owned_teams.first().pk)

@login_required()
def createteam(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            team = form.save(commit=False)
            team.owner = request.user  # set the owner of the team to the current user
            team.save()

            owner_member = TeamMember(user=team.owner, team=team)
            owner_member.save()
            return redirect('teamdetails', pk=team.id)
    else:
        form = TeamForm()
    return render(request, 'createteam.html', {'form': form})
        
@login_required()
def teamdetails(request: HttpRequest, pk: int) -> HttpResponse:
    """Displays team details and allows adding team members."""
    team = get_object_or_404(Team, pk=pk)
    members = TeamMember.objects.filter(team=team).exclude(user=team.owner)

    if request.method == 'POST':
        form = MemberForm(request.POST, instance=TeamMember(team=team))
        if form.is_valid():
            form.save()
            return redirect('teamdetails', pk=team.pk)
    else:
        form = MemberForm()
    return render(request, 'teamdetails.html', {'team': team, 'members': members, 'form': form})

@login_required()
def delete_team(request, pk):
    """Deletes a team if the user is the owner."""
    team = get_object_or_404(Team, pk=pk)

    if request.method == 'POST':
        team.delete()
        return redirect('createteam')
    return redirect('teamdetails', pk=pk)  

def register_view(request):
    if request.method == "POST":
        email = request.POST.get('username')
        password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'register.html')

        if User.objects.filter(username=email).exists():
            messages.error(request, "Email is already registered.")
            return render(request, 'register.html')

        try:
            user = User.objects.create_user(username=email, password=password)
            user.save()
        except Exception as e:
            print(f"Error creating user: {e}")

        messages.success(request, "Account created successfully. Please log in.")
        return redirect('/login/')

    return render(request, 'register.html')

def login_view(request):
    if request.method == "POST":
        email = request.POST.get('username')  
        password = request.POST.get('password')

        next_redirect = request.POST.get('next', 'dashboard')
        user = authenticate(request, username=email, password=password)
        if user:
            auth_login(request, user)
            return redirect(next_redirect)  
        else:
            messages.error(request, "Invalid email or password.")
            return render(request, "login.html", { 'next': next_redirect })  

    next_redirect = request.GET.get('next', 'dashboard')
    return render(request, 'login.html', {'next': next_redirect})

def forgot_password(request):
    """Handles password reset requests."""
    if request.method == "POST":
        email = request.POST.get("email")
        
        try:
            user = User.objects.filter(username=email).first()
            if user:
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                reset_url = request.build_absolute_uri(reverse("password_reset_confirm", kwargs={"uidb64": uid, "token": token}))

                send_mail(
                    "Password Reset Request",
                    f"Click the link below to reset your password:\n\n{reset_url}",
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
                return redirect('password_reset_sent')
            else:
                messages.error(request, "No account found with that email.")
        except Exception as e:
            print(f"Error in forgot_password: {e}")
            messages.error(request, "An error occurred. Please try again.")

    return render(request, "forgot_password.html")

def logout_view(request):
    logout(request)
    return redirect('login') 

def password_reset_sent(request):
    return render(request, "password_reset_sent.html")