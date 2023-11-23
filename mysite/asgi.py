"""
ASGI config for mysite project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os


import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import mysite.routing  # 웹소켓 라우팅을 위한 애플리케이션의 routing 모듈
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')


application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            mysite.routing.websocket_urlpatterns  # 웹소켓 URL 패턴
        )
    ),
})