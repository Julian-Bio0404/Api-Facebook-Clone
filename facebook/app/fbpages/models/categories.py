"""Category model."""

# Django
from django.db import models

# Utilities
from utils.models import FbModel


class Category(FbModel):
    """Category model."""
    
    name = models.CharField(help_text='category name', max_length=100)

    def __str__(self):
        """Return category name."""
        return str(self.name)
