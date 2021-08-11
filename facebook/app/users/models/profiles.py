"""Profile model."""

# Django
from django.db import models

# Utilities
from utils.models import FbModel


class Profile(FbModel):
    """Profile model.

    A profile holds a users public data like,
    photo and features.
    """

    user = models.OneToOneField('users.User', on_delete=models.CASCADE)
    photo = models.ImageField(
        help_text='profile photo',
        upload_to='users/photos/',
        blank=True,
        null=True
    )

    cover_photo = models.ImageField(
        help_text='profile cover photo',
        upload_to='users/cover_photos/',
        blank=True,
        null=True
    )

    about = models.TextField(
        help_text='write something about you',
        blank=True
    )

    followers = models.ManyToManyField(
        'users.User',
        blank=True,
        related_name='followers'
    )

    following = models.ManyToManyField(
        'users.User',
        blank=True,
        related_name='following'
    )

    hobby = models.CharField(
        help_text='your hobbies',
        max_length=100,
        blank=True
    )

    birth_date = models.DateTimeField(
        help_text='date of birth',
        auto_now=False,
        auto_now_add=False,
        blank=True,
        null=True
    )

    origin_country = models.CharField(
        help_text='your country of origin',
        max_length=60,
        blank=True
    )

    @property
    def full_name(self):
        "Returns the person's full name."
        return '%s %s' % (self.user.first_name, self.user.last_name)

    def __str__(self):
        """Return user's str representation."""
        return str(self.user)


class ProfileDetail(FbModel):
    """Profile detail model.

    A profile holds a users details like,
    work, education, etc.
    """
    user = models.OneToOneField('users.User', on_delete=models.CASCADE)
    profile = models.OneToOneField('users.Profile', on_delete=models.CASCADE)

    work = models.CharField(
        help_text='your current job',
        max_length=100,
        blank=True
    )

    education = models.CharField(
        help_text='last studies',
        max_length=100,
        blank=True
    )

    current_city = models.CharField(
        help_text='city ​​where you currently live',
        max_length=60,
        blank=True
    )

    web_site = models.URLField(
        help_text='personal web site',
        max_length=200,
        blank=True
    )

    social_links = models.URLField(
        help_text='social media',
        max_length=150,
        blank=True
    )

    def __str__(self):
        """Return user's str representation."""
        return str(self.user)
