# texts
Unfinished Django project that I have started a while ago when I was learning Django. It is a website similar to 9gag but for pasting texts that are converted to images with imgkit and Celery libraries. The GUI is based on Bootstrap.

How to run:
1. Install Docker with docker-compose
2. Use ``docker-compose build`` to create container images
3. Use ``docker-compose up`` to start the container
4. Run ``docker-compose exec django python manage.py collectstatic`` to find and copy all static files to ``/app/static`` directory.
5. Run ``docker-compose exec django python manage.py migrate`` to populate the PostgreSQL database with tables.
6. Run ``docker-compose exec django python manage.py createsuperuser`` ans answer a few questions to create an admin account.
5. Then go to ``http://127.0.0.1:8000`` and access the website.

List of the things that has to be done:
1. Sidebar
2. Comments
3. Comments pagination
4. User profile view
5. Edit user profile view
