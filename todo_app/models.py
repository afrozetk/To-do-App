from django.db import models
from datetime import timedelta

# Define data models:
#! TODO: We will need to work on linking these models up to a specific user account.

class Team(models.Model):
    name = models.CharField(max_length=70)
    description = models.TextField()

class TeamMember(models.Model):
    name = models.CharField(max_length=70)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

class Todo(models.Model):
    class TodoState(models.TextChoices):
        NOT_STARTED = "N", "Not Started"
        ACTIVE = "A", "Active"
        PAUSED = "P" "Paused"
        STOPPED = "S", "Stopped"

    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    due_date = models.DateField()
    category = models.CharField(max_length=50,blank=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True)

    state = models.CharField(
        max_length=7, 
        choices=TodoState, 
        default=TodoState.NOT_STARTED
    )
    start_time = models.DateTimeField(null=True)
    total_elapsed = models.DurationField(default=timedelta())

    def __str__(self):
        return self.title
