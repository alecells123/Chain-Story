"""
ASGI config for chainstory project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from linkapp.routing import websocket_urlpatterns  # Ensure this path is correct

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chainstory.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns  # Ensure this is defined in your routing
        )
    ),
})