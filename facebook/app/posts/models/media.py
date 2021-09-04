"""Media models."""

# Django
from django.db import models

# Utilities
from utils.models import FbModel



class Picture(FbModel):
    """Picture model."""

    content = models.ImageField(
        help_text='Post picture', upload_to='Images/pictures/posts/', 
        blank=True, null=True)


class Video(FbModel):
    """Video model."""

    content = models.FileField(
        help_text='Post video', upload_to='posts/videos/',
        blank=True, null=True)
