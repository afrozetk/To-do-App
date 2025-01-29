from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse
from django.contrib.auth import authenticate, logout, login as auth_login
from .forms import LoginForm, ResetPasswordForm, CreateTodoForm, TeamForm, MemberForm
from django.contrib import messages
from .models import Todo, Team, TeamMember
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required

# Define views here:

def index(request: HttpRequest) -> HttpResponse:
    return render(request, "index.html")

  
def about(request: HttpRequest) -> HttpResponse:
    return render(request, "about.html")

@login_required()
def dashboard(request: HttpRequest) -> HttpResponse:
    todos = Todo.objects.filter(user=request.user) # Fetch all Todo items linked to authenticated from the DB.
    return render(request, 'dashboard.html', {'todos': todos})

@login_required()
def todo_create(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = CreateTodoForm(request.POST, instance=Todo(user=request.user))
        if form.is_valid():
            form.save()
            return redirect('dashboard')
        else:
            print(form.errors)
    else:
        form = CreateTodoForm()  
    return render(request, 'create.html', {'form': form})

@login_required()
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
def createteam(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            team=form.save(commit=False)
            team.owner=request.user #set the owner of the team to the current user
            team.save()
            return redirect('teamdetails', pk=team.id)
    else:
        form = TeamForm()
    return render(request, 'createteam.html', {'form': form})
        

@login_required()
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
        return redirect('login')  # Replace 'login' with your login page URL pattern name

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
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            new_password = form.cleaned_data['new_password']
            
            # Check if email exists in the 'username' field
            user = User.objects.filter(username=email).first()
            if user:
                # Update the user's password
                user.password = make_password(new_password)
                user.save()

                # After saving the new password, redirect to the success page
                return redirect('password_reset_success')
            else:
                form.add_error('email', 'No user found with this email address.')  # Add error if no user found
        else:
            print("Form errors:", form.errors)
    else:
        form = ResetPasswordForm()

    return render(request, 'forgot_password.html', {'form': form}) 

def password_reset_success(request):
    # Your success page logic here
    return render(request, 'password_reset_success.html')

def logout_view(request):
    logout(request)
    return redirect('login') 