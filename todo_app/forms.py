from django import forms
from .models import Todo, Team, TeamMember
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

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
    
    #copied from chatgpt
class ResetPasswordForm(forms.Form):
    email = forms.EmailField()  # User email input
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data['email']
        # Look for the email in the 'username' field of User model
        if not User.objects.filter(username=email).exists():
            raise ValidationError("No user found with this email address.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password != confirm_password:
            raise ValidationError("Passwords do not match.")
        return cleaned_data

    
class CreateTodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'description', 'due_date', 'category', 'team']
        exclude = ['user']

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
        exclude = ['team', 'owner'] # Exclude the team field from the form since it will be filled automatically in view.

        # Define the widget styles/attributes for the form field: 
        widgets = {
            'name': forms.TextInput(attrs={
                'type': 'text', 
                'class': 'form-control', 
                'placeholder': 'Add a member'}
        )}
    def __init__(self, *args, **kwargs):
        self.team = kwargs.pop('team', None)
        super().__init__(*args, **kwargs)

    #validation for making sure the email exists in the db, used documentation and AI
    def clean_name(self):
        email = self.cleaned_data['name']
        
        # Check if the user exists by email in the username field
        try:
            user = User.objects.get(username=email) 
        except User.DoesNotExist:
            raise ValidationError("No user found with this email address.")
        
        if user == self.team.owner:
            raise ValidationError("The team owner cannot be added as a member.")

        # Check if the user is already part of this team
        if TeamMember.objects.filter(team=self.team, name=email).exists():
            raise ValidationError(f"{email} is already a member of this team.")
            
        return email
