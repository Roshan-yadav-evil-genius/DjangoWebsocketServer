"""
ASGI config for RoshanServer project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.sessions import SessionMiddlewareStack
from channels.auth import AuthMiddlewareStack
import FreelanceInstanceManager.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "RoshanServer.settings")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": SessionMiddlewareStack(
        AuthMiddlewareStack(
            URLRouter(
                FreelanceInstanceManager.routing.websocket_urlpatterns
            )
        )
    ),
})
