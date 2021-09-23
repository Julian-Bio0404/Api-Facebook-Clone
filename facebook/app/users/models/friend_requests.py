"""Friend request model."""

# Django
from django.db import models

# Utilities
from app.utils.models import FbModel


class FriendRequest(FbModel):
    """Friend request."""

    requesting_user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    
    requested_user = models.ForeignKey(
        'users.User', 
        on_delete=models.CASCADE, 
        related_name='requested_user')

    accepted = models.BooleanField(default=False)

    def __str__(self):
        """Return requesting_user and requested_user."""
        return 'from @{} to @{}'.format(
            self.requesting_user.username,
            self.requested_user.username)