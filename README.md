### Building and running the application

First configure a `.env` file based on the example shown in [.env.example](/.env.example)

When you're ready, start the application by running:
`docker compose up --build`.

The application will be available at http://127.0.0.1:8000.

If you have any issue you can try to run the DB migrations:
`docker compose run django-web python manage.py migrate`