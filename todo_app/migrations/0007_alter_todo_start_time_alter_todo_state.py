# Generated by Django 5.1.4 on 2025-01-21 04:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo_app', '0006_alter_todo_team'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='start_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='todo',
            name='state',
            field=models.CharField(choices=[('N', 'Not Started'), ('A', 'Active'), ('P', 'Paused'), ('S', 'Stopped')], default='N', max_length=7),
        ),
    ]
