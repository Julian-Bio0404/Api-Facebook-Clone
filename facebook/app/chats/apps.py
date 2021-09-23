"""Chats app."""

# Django
from django.apps import AppConfig


class ChatsConfig(AppConfig):
    """Chats app config."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app.chats'
