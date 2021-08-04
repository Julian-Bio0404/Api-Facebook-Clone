"""Notifications model admin."""

# Django
from django.contrib import admin

# Models
from notifications.models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """Notification model admin."""

    list_display = [
        'pk', 'issuing_user', 
        'receiving_user', 'message'
    ]

