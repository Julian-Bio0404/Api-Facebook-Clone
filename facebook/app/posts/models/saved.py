"""Saved models."""

# Django
from django.db import models

# Utilities
from app.utils.models import FbModel


class CategorySaved(FbModel):
    """CategorySaved model."""

    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=20)

    def __str__(self):
        """Return Category's name."""
        return self.name


class Saved(FbModel):
    """Saved model."""

    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE)

    saved_category = models.ForeignKey(
        'CategorySaved', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        """Return post saved."""
        return "{}".format(self.post)

    class Meta:
        """Meta options."""
        ordering = ['-created']