""""Notification models."""

# Django
from django.db import models

# Utilities
from utils.models import FbModel


class Notification(FbModel):
    """Notification model.

    a notification is a message that alerts a user when 
    another user interacts with the content of him
    """

    issuing_user = models.ForeignKey(
        'users.User', 
        null=True,
        on_delete=models.SET_NULL
    )

    receiving_user = models.ForeignKey(
        'users.User', 
        on_delete=models.CASCADE, 
        related_name='receiving_user'
    )

    message = models.CharField(
        help_text='notification message',
         max_length=200
    )

    def __str__(self):
        """Return issuing_user and message"""
        return '@{} {}'.format(self.issuing_user.username, self.message) 

    class Meta:
        """Meta options."""
        ordering = ['-created']