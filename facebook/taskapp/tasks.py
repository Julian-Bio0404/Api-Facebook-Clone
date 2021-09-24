"""Celery tasks."""

# Utilities
from datetime import timedelta
import jwt

# Django
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone

# Celery
from celery import shared_task

# Models
from app.users.models import User


def token_generation(user, type):
    """Create JWT token."""
    exp_date = timezone.now() + timedelta(days=3)
    payload = {
        'user': user.username,
        'exp': int(exp_date.timestamp()),
        'type': type}
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token


@shared_task 
def send_confirmation_email(user_pk):
    """Send account verification link to given user."""
    user = User.objects.get(pk=user_pk)
    type = 'email_confirmation'
    token = token_generation(user, type)
    subject = 'Welcome @{}! Verify your account'.format(user.username)
    from_email = 'Facebook <Facebook.com>'
    content = render_to_string(
        'users/account_verification.html', {'token': token, 'user': user})
    msg = EmailMultiAlternatives(subject, content, from_email, [user.email])
    msg.attach_alternative(content, 'text/html')
    msg.send()


@shared_task 
def send_restore_password_email(user_pk):
    """Send restore password link to given user."""
    user = User.objects.get(pk=user_pk)
    type = 'restore_password'
    token = token_generation(user, type)
    subject = 'Update your password'
    from_email = 'Facebook <Facebook.com>'
    content = render_to_string(
        'users/restore_password.html', {'token': token, 'user': user})
    msg = EmailMultiAlternatives(subject, content, from_email, [user.email])
    msg.attach_alternative(content, 'text/html')
    msg.send()
