from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta, timezone

# Define data models:
#! TODO: We will need to work on linking these models up to a specific user account.

class Team(models.Model):
    name = models.CharField(max_length=70)
    description = models.TextField()
    #v1.2 create owner field 
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=1)

    def __str__(self):
        return self.name

class TeamMember(models.Model):
    name = models.CharField(max_length=70)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    

class TodoState(models.TextChoices):
        NOT_STARTED = "N", "Not Started"
        ACTIVE = "A", "Active"
        PAUSED = "P", "Paused"
        STOPPED = "S", "Stopped"

class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=1)
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
    start_time = models.DateTimeField(null=True, blank=True)
    total_elapsed = models.DurationField(default=timedelta())


    def relative_start(self) -> str:
        """
            Calculate the total elapsed timer based on the logged time and any currently active interval
            from the start time. Then create a relative UTC starting time based on the total elapsed time
            as an offset (as if the timer were one continuos interval).

            Returns:
                str: an UTC starting time represented as an ISO 8601 string to be used as a reference on the frontend.
        """
        now = datetime.now(timezone.utc)
        current_interval_time = now - (self.start_time or now)
        elapsed_offset = self.total_elapsed + current_interval_time

        # The date representing the start time relative to now assuming the elapsed time were continuous.
        relative_start = now - elapsed_offset
        # # Return the starting time as an iso string to be used in frontend js.
        return relative_start.isoformat()
    

    # I asked AI about possible options to updating multiple properties automatically when one is changed.
    # I then consulted the Django documentation for practices on overriding the model save method:
    # https://docs.djangoproject.com/en/5.1/topics/db/models/#overriding-predefined-model-methods
    def save(self, **kwargs):
        if self.pk: # Check if the object being saved already exists in the DB (is being updated not added).
            old = Todo.objects.get(pk=self.pk)

            # If the state of the todo item is modified, then we perform the appropriate actions based on
            # the type of state transition to start, stop, save, or clear the timer.
            if self.state != old.state:
                match (old.state, self.state): # Match for the type of transition from old state -> new state.
                    case (TodoState.STOPPED, TodoState.ACTIVE):
                        self.total_elapsed = timedelta()
                        self.start_time = datetime.now(timezone.utc)
                    case (_, TodoState.ACTIVE):
                        self.start_time = datetime.now(timezone.utc)
                    case (_, TodoState.STOPPED | TodoState.PAUSED):
                        if self.start_time is not None:
                            time_diff = datetime.now(timezone.utc) - self.start_time
                            self.total_elapsed += time_diff
                            self.start_time = None
                    case _:
                        self.total_elapsed = timedelta()
                        self.start_time = None
                
                # For optimization, the documentation recommends adding the modified items to the `updated_fields`
                # property if it has been predefined.
                if (updated := kwargs.get("updated_fields")) is not None:
                    kwargs["updated_fields"] = {"start_time", "total_elapsed"}.union(updated)
            
        super().save(**kwargs) # Calling the predefined save implementation to perform DB operations.


    def __str__(self):
        return self.title
