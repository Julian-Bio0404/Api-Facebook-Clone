"""Comment model."""

# Django 
from django.db import models

# Utilities
from utils.models import FbModel


class Comment(FbModel):
    """Comment model."""

    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    profile = models.ForeignKey('users.Profile', on_delete=models.CASCADE)
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE)

    text = models.TextField(help_text='write a comment', max_length=250)
    reactions = models.IntegerField(default=0)

    def __str__(self):
        """Return username, post title and comment."""
        return '@{} has commented {} on {}'.format(
            self.user.username, 
            self.text, 
            self.post
        )