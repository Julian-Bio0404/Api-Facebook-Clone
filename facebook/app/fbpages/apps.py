"""Fbpages app."""

# Django
from django.apps import AppConfig


class FbpagesConfig(AppConfig):
    """Fbpages app config."""
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app.fbpages'
