from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse

# Define views here:

def index(request: HttpRequest) -> HttpResponse:
    return render(request, "index.html")

def about(request: HttpRequest) -> HttpResponse:
    return render(request, "about.html")

def team_details_page(request: HttpRequest) -> HttpResponse:
    return render(request, "team.html")

def login(request: HttpRequest) -> HttpResponse:
    return render(request, "login.html")


def create_todo_page(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            # Save the form to create a new task
            form.save()
            # Redirect to the desired page, e.g., the dashboard
            return redirect('dashboard_page')  # Use the name of the URL pattern
    else:
        form = TaskForm()

    return render(request, 'create_todo_page.html', {'form': form})

