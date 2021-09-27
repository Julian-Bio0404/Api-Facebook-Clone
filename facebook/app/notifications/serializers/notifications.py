"""Notification serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from app.notifications.models import Notification


class NotificationModelSerializer(serializers.ModelSerializer):
    """Notification model serializer."""

    issuing_user = serializers.StringRelatedField(read_only=True)
    receiving_user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        """Meta options."""
        model = Notification
        fields = [
            'issuing_user', 'receiving_user', 
            'message', 'created'
        ]

        read_only_fields = [
            'receiving_user', 'receiving_user'
        ]
