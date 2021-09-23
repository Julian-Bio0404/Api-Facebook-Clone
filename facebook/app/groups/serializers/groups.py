"""Groups serializers."""

# Django REST Framework
from rest_framework import serializers

# Model
from app.groups.models import Group


class GroupModelSerializer(serializers.ModelSerializer):
    """Group model serializer."""
    
    class Meta:
        """Meta options."""
        model = Group
        fields = [
            "name", "slug_name",
            "about", "cover_photo",
            "is_public",
        ]

        read_only_fields = [
            "is_public"
        ]
