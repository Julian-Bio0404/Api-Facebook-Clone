"""Task app."""

# Django
from django.apps import AppConfig


class TaskappConfig(AppConfig):
    """Task app config."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'taskapp'