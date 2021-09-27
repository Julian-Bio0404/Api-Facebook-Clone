"""Thread models."""

# Django
from django.db import models

# Manager
from app.chats.managers import ThreadManager

# Utils
from app.utils.models import FbModel


class Thread(FbModel):
    """
    Thread model.
    This model handle the channels for communicate
    users one to one or between a user and a group.
    """
    
    THREAD_TYPE = (
        ('personal', 'Personal'),
        ('group', 'Group')
    )

    name = models.CharField(max_length=50, null=True, blank=True)

    thread_type = models.CharField(
        max_length=15, choices=THREAD_TYPE, default='group')

    users = models.ManyToManyField('users.User')

    objects = ThreadManager()

    def __str__(self) -> str:
        if self.thread_type == 'personal' and self.users.count() == 2:
            return f'{self.users.first()} and {self.users.last()}'
        return f'{self.name}'
