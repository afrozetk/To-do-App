from django import forms

class createForm(forms.Form):
    title = forms.CharField(label='Title', max_length=200)
    description = forms.CharField(label='Description', required=False)
    due_date = forms.DateTimeField(label='Due Date')
    category = forms.CharField(label='Category', max_length=50,required=False)
    # teams = forms.ForeignKey(Team, on_delete=models.CASCADE,required=False)

         