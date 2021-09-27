"""Routing configuration."""

# Django
from django.urls import path

# Channels
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

# Consumers
from app.chats.consumers import ChatConsumer, EchoConsumer

# Middlewares
from app.chats.middlewares import TokenAuthMiddleware


application = ProtocolTypeRouter({
    'websocket': TokenAuthMiddleware(
        AuthMiddlewareStack(
            URLRouter([
                path('ws/chats/<str:username>/', ChatConsumer),
                path('ws/chats/', EchoConsumer)
            ]))
        )
})