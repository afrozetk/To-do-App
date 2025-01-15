from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.

class Todo(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateTimeField(default=timezone.now)
    category = models.CharField(max_length=50,blank=True)
    team = models.CharField(max_length=50,blank=True)

    def __str__(self):
        return self.title