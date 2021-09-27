"""Routing configuration."""

# Django
from django.urls import path

# Channels
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

# Consumers
from app.chats.consumers import ChatConsumer, EchoConsumer


application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter([
            path('ws/chats/<str:username>/', ChatConsumer),
            path('ws/chats/', EchoConsumer)
        ])
    )
})