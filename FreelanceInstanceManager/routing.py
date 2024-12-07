from .Consumer import *
from django.urls import path

websocket_urlpatterns = [
    path("ws/", JsonConsumer.as_asgi()),
]