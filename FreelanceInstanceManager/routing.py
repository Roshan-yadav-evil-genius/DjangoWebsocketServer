from .Consumer import *
from django.urls import path,re_path


websocket_urlpatterns = [
    re_path(r"ws/(?P<room_name>\w+)/$", JsonConsumer.as_asgi()),
]