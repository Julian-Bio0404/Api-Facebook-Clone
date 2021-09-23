"""Membership model."""

# Django
from django.db import models

# Utilities
from app.utils.models import FbModel


class Membership(FbModel):
    """
    Membership model.
    A membership is the model that holds the 
    relationship between a user and a group.
    """

    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    profile = models.ForeignKey("users.Profile", on_delete=models.CASCADE)
    group = models.ForeignKey("groups.Group", on_delete=models.CASCADE)

    is_admin = models.BooleanField(
        default=False, help_text='Group admin can have action on a group.')

    invited_by = models.ForeignKey(
        "users.User", on_delete=models.SET_NULL,
        null=True, related_name='invited_by')

    is_active = models.BooleanField(
        default=False, 
        help_text='Only active users are allowed to interact in the group.')

    def __str__(self):
        """Return username and slugname."""
        return "@{} at #{}".format(self.user.username, self.group.slug_name)
