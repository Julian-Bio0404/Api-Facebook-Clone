"""Groups app."""

# Django
from django.apps import AppConfig


class GroupsConfig(AppConfig):
    """Groups app config."""
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app.groups'
