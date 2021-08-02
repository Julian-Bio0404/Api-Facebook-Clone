"""Reactions models."""

# Django
from django.db import models

# Utilities
from utils.models import FbModel


class ReactionPost(FbModel):
    """Reaction Post model."""

    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    profile = models.ForeignKey('users.Profile', on_delete=models.CASCADE)

    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE)

    # Reaction choices
    REACTIONS = [
        ('LIKE', 'like'), ('LOVE', 'love'),
        ('CARE', 'care'), ('HAHA', 'haha'),
        ('SAD', 'sad'), ('ANGRY', 'angry')
    ]

    reaction = models.CharField(
        help_text='react to a post', 
        max_length=5, 
        choices=REACTIONS
    )

    def __str__(self):
        """Return user, post and reaction."""
        return '@{} reacted to your post {}'.format(
            self.user.username, 
            self.post.pk
        )


class ReactionComment(FbModel):
    """Reaction Comment model."""

    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    profile = models.ForeignKey('users.Profile', on_delete=models.CASCADE)

    comment = models.ForeignKey('posts.Comment', on_delete=models.CASCADE)

    # Reaction choices
    REACTIONS = [
        ('LIKE', 'like'), ('LOVE', 'love'),
        ('CARE', 'care'), ('HAHA', 'haha'),
        ('SAD', 'sad'), ('ANGRY', 'angry')
    ]

    reaction = models.CharField(
        help_text='react to a comment', 
        max_length=5, 
        choices=REACTIONS
    )

    def __str__(self):
        """Return user, post and reaction."""
        return '@{} reacted to your comment {}'.format(
            self.user.username, 
            self.comment.text
        )
