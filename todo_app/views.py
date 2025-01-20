from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse
from django.contrib.auth import authenticate, logout
from .forms import LoginForm
from django.contrib import messages
from .forms import CreateTodoForm, ResetPasswordForm
from .models import Todo
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login
from django.core.exceptions import ObjectDoesNotExist

# Define views here:

def index(request: HttpRequest) -> HttpResponse:
    return render(request, "index.html")

def about(request: HttpRequest) -> HttpResponse:
    return render(request, "about.html")
  
def dashboard_view(request):
  todos = Todo.objects.all()  # Fetch all ToDo items from the database
  return render(request, 'dashboard.html', {'todos': todos})


def login_view(request: HttpRequest) -> HttpResponse:
    return render(request, "login.html")


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
def login_views(request):
    if request.method == "POST":
        email = request.POST.get('username')  # Captures email as username
        password = request.POST.get('password')
        
        print(f"Attempting to login with Email: {email} and Password: {password}")

        # Authenticate user
        user = authenticate(request, username=email, password=password)
        if user is not None:
            print(f"Authentication successful for {email}")
            auth_login(request, user)  # Log the user in
            return redirect('dashboard_view')  # Redirect to the dashboard
        else:
            print(f"Authentication failed for {email}")
            messages.error(request, "Invalid email or password. Please check your credentials and try again.")
            print(f"Failed login attempt: {email} with password {password}")
            return render(request, "login.html")  # Stay on the login page if authentication fails
    
    return render(request, 'login.html')