"""Page Invitations model."""

# Django
from django.db import models

# Utilities
from app.utils.models import FbModel


class PageInvitation(FbModel):
    """
    Page Invitation model.
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
    
    page = models.ForeignKey('fbpages.Page', on_delete=models.CASCADE, null=True)

    used = models.BooleanField(default=False)

    def __str__(self):
        """Return inviting_user and guest_user."""
        return "from: {}, to: {}".format(self.inviting_user, self.guest_user)