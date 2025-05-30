# Generated by Django 5.1.4 on 2025-01-29 04:51

from django.db import migrations

# Here we want to migrate the member model use the new user forign key instead of the raw text name to reduce data duplication.
# We need to migrate the existing member names if they are valid emails associated with a user (otherwise we will just delete them).
# I referenced the Django documentation on data migration https://docs.djangoproject.com/en/5.1/topics/migrations/#data-migrations
def link_member_user(apps, schema_editor):
    # Get the model references:
    TeamMember = apps.get_model("todo_app", "TeamMember")
    User = apps.get_model('auth', 'User')

    for member in TeamMember.objects.all(): # Loop over each member and migrate the data.
        try: 
            member.user = User.objects.get(username=member.name) # Update the user to match the email.
            member.save()
        except User.DoesNotExist:
            member.delete() # Delete the team member if the name is not a valid user email.


class Migration(migrations.Migration):
    dependencies = [
        ('todo_app', '0011_member_add_user'),
    ]

    operations = [
        migrations.RunPython(link_member_user),
    ]
