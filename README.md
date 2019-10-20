# texts
Unfinished Django project that I have started a while ago when I was learning Django. It is a website similar to 9gag but for pasting texts that are converted to images with imgkit and Celery libraries. The GUI is based on Bootstrap.

How to run:
1. Install Docker along with docker-compose.
1. Use ``docker-compose build`` to create container images.
1. Use ``docker-compose up`` to start the container.
1. Run ``docker-compose exec django python manage.py collectstatic`` to find and copy all static files to ``/app/static`` directory.
1. Run ``docker-compose exec django python manage.py migrate`` to populate the PostgreSQL database with tables.
1. Run ``docker-compose exec django python manage.py createsuperuser`` ans answer a few questions to create an admin account.
1. Then go to ``http://127.0.0.1:8000`` and access the website.

List of the things that has to be done:
1. Comments
1. Comments pagination
1. User profile view
1. REST API
