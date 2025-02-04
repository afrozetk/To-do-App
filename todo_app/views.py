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
from django.http import JsonResponse

# Define views here:

def index(request: HttpRequest) -> HttpResponse:
    return render(request, "index.html")

  
def about(request: HttpRequest) -> HttpResponse:
    return render(request, "about.html")
@login_required()
def dashboard(request: HttpRequest) -> HttpResponse:
    # Get tasks created by the user
    user_tasks = Todo.objects.filter(user=request.user)

    # Get tasks assigned to the user
    assigned_tasks = Todo.objects.filter(assigned=request.user)

    # Combine the tasks
    todos = user_tasks | assigned_tasks  # Use the `|` operator to combine the querysets

    return render(request, 'dashboard.html', {'todos': todos})

# @login_required()
# def dashboard(request: HttpRequest) -> HttpResponse:
#     todos = Todo.objects.filter(user=request.user) # Fetch all Todo items linked to authenticated from the DB.

#     # Get all the teams the user is apart of and add any items assigned to
#     # those teams to be displayed on their dashboard.
#     users_teams = TeamMember.objects.filter(user=request.user)
#     todos = todos.union(*[
#         Todo.objects.filter(team=user_member.team).exclude(user=request.user) 
#         for user_member in users_teams
#     ])
#      # Filter tasks based on the assigned user
#     assigned_to_user = todos.filter(assigned=request.user)

#     # Combine tasks for the logged-in user (both created and assigned)
#     todos = todos.union(assigned_to_user)

#     return render(request, 'dashboard.html', {'todos': todos})
# v1.3 added assigned field - edit to add assigned field pending
@login_required()
def todo_create(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = CreateTodoForm(request.POST, instance=Todo(user=request.user), user=request.user)
        if form.is_valid():
            todo=form.save(commit=False)
            assigned_user = form.cleaned_data.get('assigned')
            if assigned_user:
                todo.assigned = assigned_user
            todo.save()
            return redirect('dashboard')
        else:
            print(form.errors)
    else:
        form = CreateTodoForm(user=request.user)  
    return render(request, 'create.html', {'form': form})


@login_required
def get_team_members(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    members = TeamMember.objects.filter(team=team).values('user__id', 'user__username') # Optimized query
    member_list = [{'id': m['user__id'], 'username': m['user__username']} for m in members]
    return JsonResponse(member_list, safe=False)

 # v1.3 added assigned field - edit to add assigned field pending

@login_required()
def todo_edit(request, id):
    todo=get_object_or_404(Todo, id=id)
    if request.method == 'POST':
        form = CreateTodoForm(request.POST, instance=todo, user=request.user)
        if form.is_valid():
            todo=form.save(commit=False)
            assigned_user = form.cleaned_data.get('assigned')
            if assigned_user:
                todo.assigned = assigned_user
    
            todo.save()
            return redirect('dashboard')
    else:
        form = CreateTodoForm(instance=todo, user=request.user)
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
    todo = Todo.objects.get(id=id)
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
            team=form.save(commit=False)
            team.owner=request.user #set the owner of the team to the current user
            team.save()

            owner_member = TeamMember(user=team.owner, team=team)
            owner_member.save()
            return redirect('teamdetails', pk=team.id)
    else:
        form = TeamForm()
    return render(request, 'createteam.html', {'form': form})
        

@login_required()
def teamdetails(request: HttpRequest, pk: int) -> HttpResponse:
    # Get team by ID and it's associated members from the DB model:
    team = get_object_or_404(Team, pk=pk)
    members = TeamMember.objects.filter(team=team).exclude(user=team.owner)

    if request.method == 'POST':
        # Create form model with the missing team foreign key so it validates properly.
        form = MemberForm(
            request.POST,
            instance=TeamMember(team=team)
        )
        if form.is_valid():
            form.save()
            return redirect('teamdetails', pk=team.pk)
    else:
        form = MemberForm()
    return render(request, 'teamdetails.html', {'team': team, 'members': members, 'form': form})

@login_required()
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


#used chat gpt for this code
def register_view(request):
    if request.method == "POST":
        email = request.POST.get('username')
        password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        # Validate that passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            
            return render(request, 'register.html')

        # Validate email uniqueness
        if User.objects.filter(username=email).exists():
            messages.error(request, "Email is already registered.")
            return render(request, 'register.html')

        # Create the user
        try:
            user = User.objects.create_user(username=email, password=password)
            user.save()
            print(f"User created: {user.username}")  # This will print to the console
        except Exception as e:
            print(f"Error creating user: {e}")  # If there's any error, it'll print here


        # Redirect to login page after successful registration
        messages.success(request, "Account created successfully. Please log in.")
        return redirect('/login/')

    return render(request, 'register.html')

#written based off chatgpt code
def login_view(request):
    if request.method == "POST":
        email = request.POST.get('username')  # Captures email as username
        password = request.POST.get('password')
        
        print(f"Attempting to login with Email: {email} and Password: {password}")

        next_redirect = request.POST.get('next', 'dashboard')
        # Authenticate user
        user = authenticate(request, username=email, password=password)
        if user is not None:
            print(f"Authentication successful for {email}")
            auth_login(request, user)  # Log the user in
            return redirect(next_redirect)  # Redirect to the dashboard
        else:
            print(f"Authentication failed for {email}")
            messages.error(request, "Invalid email or password. Please check your credentials and try again.")
            print(f"Failed login attempt: {email} with password {password}")
            return render(request, "login.html", { 'next': next_redirect })  # Stay on the login page if authentication fails
    
    next_redirect = request.GET.get('next', 'dashboard')
    return render(request, 'login.html', {'next': next_redirect})

def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get("email")
        
        try:
            user = User.objects.filter(username=email).first()
            
            if user:
                # Create a targeted reset url with user reference token: 
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                reset_url = request.build_absolute_uri(reverse("password_reset_confirm", kwargs={"uidb64": uid, "token": token}))
                
                # Send out an email with the reset link to the user: 
                send_mail(
                    "Password Reset Request",
                    f"Click the link below to reset your password:\n\n{reset_url}",
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )

                # Redirect to the new confirmation page
                return redirect('password_reset_sent')
            else:
                return render(request, "forgot_password.html", {"error_message": "No account found with that email."})
        except Exception as e:
            print(f"Error in forgot_password: {e}")
            return render(request, "forgot_password.html", {"error_message": "An error occurred. Please try again."})

    return render(request, "forgot_password.html")

def logout_view(request):
    logout(request)
    return redirect('login') 

def password_reset_sent(request):
    return render(request, "password_reset_sent.html")