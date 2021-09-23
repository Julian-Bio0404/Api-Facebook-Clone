"""Posts app."""

# Django
from django.apps import AppConfig


class PostsConfig(AppConfig):
    """Posts app config."""
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app.posts'
