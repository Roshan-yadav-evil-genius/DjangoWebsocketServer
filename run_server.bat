@echo off
set DJANGO_SETTINGS_MODULE=RoshanServer.settings
daphne -b 0.0.0.0 -p 8000 RoshanServer.asgi:application