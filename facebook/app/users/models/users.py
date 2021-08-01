"""User model."""

# Django
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

# Utilities
from utils.models import FbModel


class User(FbModel, AbstractUser):
    """User model.
    Extend from Django's Abstract User and add some extra fields.
    """

    email = models.EmailField(
        'email address',
        unique=True,
        error_messages={
            'unique': 'A user with that email already exists.'
            }
    )

    # phone number validator
    phone_regex = RegexValidator(
        regex=r"\+?1?\d{9,15}$",
        message='Phone number must be entered in the format: +999999999. Up to 15 digits allowed.'
    )

    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=17, 
        blank=True
    )

    is_verified = models.BooleanField(
        'verified',
        default=False,
        help_text=(
            'Set to true when the user have verified its email add'
        )
    )

    # Username configuration
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    def __str__(self):
        """Return username."""
        return self.username

    def get_short_name(self):
        """Return username."""
        return self.username
        