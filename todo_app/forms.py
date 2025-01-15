
from django import forms
from .models import Todo  

class CreateForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'description', 'due_date', 'category', 'team']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'team': forms.Select(attrs={'class': 'form-control'})
        }


            # def clean_due_date(self):
            #     due_date = self.cleaned_data['due_date']
            #     if due_date < timezone.now().date():  
            #         raise ValidationError("The due date cannot be in the past.")
            #     return due_date
