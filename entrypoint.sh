
python manage.py migrate
gunicorn project_manager.wsgi:application --bind 0.0.0.0:8000