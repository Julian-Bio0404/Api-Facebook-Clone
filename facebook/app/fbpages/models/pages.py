"""Pages model."""

# Django
from django.core.validators import RegexValidator
from django.db import models

# Utilities
from utils.models import FbModel


class Page(FbModel):
    """Pages model."""
    
    name = models.CharField(help_text='pages name', max_length=130)

    slug_name = models.SlugField(
        help_text='slug name', 
        unique=True, max_length=60)

    creator = models.OneToOneField(
        'users.User', on_delete=models.SET_NULL, null=True)

    admins = models.ManyToManyField(
        'users.User', blank=True, related_name='admins')

    photo = models.ImageField(
        help_text='pages profile photo',
        upload_to='pages/photos/',
        blank=True, null=True)

    cover_photo = models.ImageField(
        help_text='pages profile cover photo',
        upload_to='pages/cover_photos/',
        blank=True, null=True)

    about = models.TextField(
        help_text='write something about page', blank=True)

    category = models.ForeignKey(
        'fbpages.Category', on_delete=models.SET_NULL, null=True)

    likes = models.IntegerField(
        help_text="page's likes", blank=True, null=True)

    page_followers = models.ManyToManyField(
        'users.User', blank=True, related_name='page_followers')

    def __str__(self):
        """Return page's name."""
        return str(self.name)


class PageDetail(FbModel):
    """Page detail model."""

    page = models.OneToOneField('fbpages.Page', on_delete=models.CASCADE)
    direction = models.CharField(help_text='pages name', max_length=110)

    # phone number validator
    phone_regex = RegexValidator(
        regex=r"^\+1?\d{1,4}[ ]\d{10}$",
        message='Phone number must be entered in the format: +99 9999999999. Up to indicative + 10 digits allowed.')

    phone_number = models.CharField(
        validators=[phone_regex], max_length=17, blank=True)

    web_site = models.URLField(
        help_text='page web site', max_length=200, blank=True)

    social_links = models.URLField(
        help_text='social media', max_length=150, blank=True)

    def __str__(self):
        """Return page's name."""
        return str(self.page)
