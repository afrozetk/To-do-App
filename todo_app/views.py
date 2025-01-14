from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from .forms import createForm
from .models import create

# Define views here:

def index(request: HttpRequest) -> HttpResponse:
    return render(request, "index.html")

def create(request):
    if request.method == 'POST':
        form = createForm(request.POST)
        if form.is_valid():
            form.save()
            create.objects.create(
        title=form.cleaned_data['title'],
        description=form.cleaned_data['description'],
        due_date=form.cleaned_data['due_date'],
        category=form.cleaned_data['category'], 
        )
            return render(request, "dashboard.html")
    form = createForm()
    return render(request, "create.html", {'createform': form})