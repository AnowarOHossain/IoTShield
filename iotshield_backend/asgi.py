"""
ASGI config for IoTShield project.
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iotshield_backend.settings')

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    # Add WebSocket routing here if needed
    # "websocket": AuthMiddlewareStack(
    #     URLRouter(
    #         # websocket_urlpatterns
    #     )
    # ),
})
