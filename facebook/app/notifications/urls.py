"""Notifications URLs."""

# Django
from django.urls import path

# Views
from .views import list_notifications, detail_notification


urlpatterns = [
    path('notifications/', list_notifications),
    path('notifications/<int:pk>/', detail_notification)

]