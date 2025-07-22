set DJANGO_SETTINGS_MODULE=RoshanServer.settings 
daphne -b 0.0.0.0 -p 8000 RoshanServer.asgi:application

python manage.py shell

from django.contrib.auth import get_user_model
User = get_user_model()
User.objects.create_user(username='your_username', password='your_password')

 nohup ./venv/bin/daphne -b 0.0.0.0 -p 8000 RoshanServer.asgi:application > daphne.log 2>&1 &

 ps aux | grep daphne

kill <PID>
