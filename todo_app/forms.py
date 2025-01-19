from django import forms
from .models import Todo, Team, TeamMember

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150, 
        required=True, 
        widget=forms.TextInput(attrs={'placeholder': 'Enter your username'})
    )
    password = forms.CharField(
        required=True, 
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'})
    )

    
class CreateTodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'description', 'due_date', 'category', 'team']

        # Referenced documentation and AI to figure out how to create a select field for forign key:
        team = forms.ModelChoiceField(
            queryset=Team.objects.all(),
            empty_label="team"
        )

        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'category': forms.TextInput(attrs={'class': 'form-control'}),
            'team': forms.Select(attrs={'class': 'form-control'})
        }

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'description']

class MemberForm(forms.ModelForm):
    class Meta:
        model = TeamMember
        fields = ['name', 'team'] 