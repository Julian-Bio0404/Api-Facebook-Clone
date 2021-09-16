"""Page Invitations model."""

# Django
from django.db import models

# Utilities
from utils.models import FbModel


class PageInvitation(FbModel):
    """Page Invitation model.

    A page invitation is an invitation from 
    an user to another to follow a page.
    """
    
    inviting_user = models.ForeignKey(
        'users.User', on_delete=models.CASCADE,
        help_text='User that is providing the invitation.')

    guest_user = models.ForeignKey(
        'users.User', on_delete=models.CASCADE,
        help_text='User that used the invitation.',
        null=True, related_name='guest_user')

    used = models.BooleanField(default=False)

    def __str__(self):
        """Return code and group."""
        return "from: {}, to: {}".format(self.sent_by.username, self.used_by.username)