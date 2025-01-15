
from django import forms
from .models import Create  

class CreateForm(forms.ModelForm):
    class Meta:
        model = Create
        fields = ['title', 'description', 'due_date', 'category', 'team']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'team': forms.Select(attrs={'class': 'form-control'})
        }
