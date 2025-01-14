from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

# Define views here:

def index(request: HttpRequest) -> HttpResponse:
    return render(request, "index.html")


def about(request: HttpRequest) -> HttpResponse:
    return render(request, "about.html")
