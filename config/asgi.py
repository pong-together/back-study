import os

from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

import chat

os.environ.setdefault('DJANGO_SETTING_MODULE', 'config.settings')

django_asgi_app = get_asgi_application()

from channels.routing import ProtocolTypeRouter, URLRouter

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket":
            AuthMiddlewareStack(
                AllowedHostsOriginValidator(
                    URLRouter(
                        chat.routing.websocket_urlpatterns
                    )
                )
            )
    }
)