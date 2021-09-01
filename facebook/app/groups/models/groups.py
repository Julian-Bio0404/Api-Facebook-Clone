"""Group model."""

# Django
from django.db import models

# Utilities
from utils.models import FbModel


class Group(FbModel):
    """Group model.

    A group is where users will be able 
    to share content between members.
    """

    name = models.CharField(help_text='group name', max_length=130)

    slug_name = models.SlugField(
        help_text='slug name', 
        unique=True, max_length=60)

    about = models.CharField(
        help_text='group description',
        max_length=200, blank=True)

    cover_photo = models.ImageField(
        help_text='group picture', 
        upload_to='groups/pictures/', 
        blank=True, null=True)

    members = models.ManyToManyField(
        'users.User',
        through='groups.Membership',
        through_fields=('group', 'user'))

    is_public = models.BooleanField(
        default=True,
        help_text='Public groups can be found by other users')

    def __str__(self):
        """Return group name."""
        return self.name