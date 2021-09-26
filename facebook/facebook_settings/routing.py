"""Routing configuration."""

# Django
from django.urls import path

# Channels
from channels.routing import ProtocolTypeRouter, URLRouter

# Consumers
from app.chats.consumers import EchoConsumer


application = ProtocolTypeRouter({
    'websocket': URLRouter([
        path('ws/chats/', EchoConsumer)
    ])
})