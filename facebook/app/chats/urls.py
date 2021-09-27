"""Chat Urls."""

# Django
from django.urls import path

# Views
from app.chats.views import ThreadView


urlpatterns = [
    path('chats/<str:username>/', ThreadView.as_view())
]