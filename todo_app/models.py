from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.
class create(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateTimeField(default=timezone.now)
    category = models.CharField(max_length=50)
    # teams = models.ForeignKey(Team, on_delete=models.CASCADE)

def __str__(self):
    return self.title