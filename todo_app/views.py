from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

# Define views here:

def index(request: HttpRequest) -> HttpResponse:
    return render(request, "index.html")


def about(request: HttpRequest) -> HttpResponse:
    return render(request, "about.html")

def createteams(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        teamname = request.POST.get('teamname')
        description = request.POST.get('description')
    return render(request, "createteams.html")

def register(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        passwordconfirm = request.POST.get('passwordconfirm')
    return render(request, "register.html")