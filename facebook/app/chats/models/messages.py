"""Message models."""

# Django
from django.db import models

# Utils
from app.utils.models import FbModel


class Message(FbModel):
    """Message model."""

    thread = models.ForeignKey('Thread', on_delete=models.CASCADE)
    sender = models.ForeignKey('users.User', on_delete=models.CASCADE)
    text = models.TextField(blank=False, null=False)

    def __str__(self) -> str:
        return f'From <Thread - {self.thread}>'