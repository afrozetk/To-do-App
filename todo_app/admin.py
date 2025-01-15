from django.contrib import admin
from .models import Todo, Team, TeamMember 

# Register your models here.
admin.site.register(Todo)
admin.site.register(Team)
admin.site.register(TeamMember)