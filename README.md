
📝 To-Do App (Django + PostgreSQL)

A full-stack task management app built with Django and PostgreSQL.

Developed as part of CSC 394 - Software Projects at DePaul University.

🚀 Features

User login, registration, and password reset
Create, edit, and delete personal or team tasks
Team creation and management
Responsive UI 

🛠 Tech Stack

Django (Python)
PostgreSQL
HTML / CSS / Bootstrap


### Building and running the application

First configure a `.env` file based on the example shown in [.env.example](/.env.example)

When you're ready, start the application by running:
`docker compose up --build`

or in development you can use the watch attribute to automatically watch for and sync file
changes into they running docker container to make testing changes easier:

`docker compose up --build --watch`.

Visit http://127.0.0.1:8000/ to use the app!

If you have any issue you can try to run the DB migrations:
`docker compose run django-web python manage.py migrate`

