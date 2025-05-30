# Generated by Django 5.1.5 on 2025-01-31 21:17

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo_app', '0016_todo_assigned_to'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='todo',
            name='assigned_to',
        ),
        migrations.AddField(
            model_name='todo',
            name='assigned',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assigned', to=settings.AUTH_USER_MODEL),
        ),
    ]
