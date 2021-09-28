""""Notification models."""

# Django
from django.db import models

# Utilities
from app.utils.models import FbModel


class Notification(FbModel):
    """
    Notification model.
    A notification is a message that alerts a user when 
    another user interacts with the content of him.
    """

    issuing_user = models.ForeignKey(
        'users.User', null=True, on_delete=models.SET_NULL)

    receiving_user = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, related_name='receiving_user')

    message = models.CharField(
        help_text='notification message', max_length=200)

    NOTIFICATION_TYPE = (
        ('group invitation', 'Group Invitation'),
        ('page invitation', 'Page Invitation'),
        ('reaction post', 'Reaction Post'),
        ('post', 'Post'),
        ('comment post', 'Comment Post'),
        ('reaction comment', 'Reaction Comment'),
        ('mention', 'Mention'),
        ('friend request', 'Friend Request'),
        ('friend accept', 'Friend Accept')
    )

    notification_type = models.CharField(max_length=16, choices=NOTIFICATION_TYPE)
    
    object_id = models.IntegerField(
        help_text="object's id on which the notification was generated.", null=True)


    def __str__(self):
        """Return issuing_user and message"""
        return '@{}: {}'.format(self.issuing_user.username, self.message) 

    class Meta:
        """Meta options."""
        ordering = ['-created']
