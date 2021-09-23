"""Shared model."""

# Django
from django.db import models

# Utilities
from app.utils.models import FbModel


class Shared(FbModel):
    """
    Shared model.
    holds the user who reposted and the repost
    """

    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE)

    about = models.TextField(
        help_text='user text about the post reposted.', blank=True)

    def __str__(self):
        """Return about and username"""
        return "{} by @{}".format(self.about, self.user.username)
