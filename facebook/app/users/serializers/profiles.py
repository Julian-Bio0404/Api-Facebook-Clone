"""Profile serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from users.models import Profile, ProfileDetail


class ProfileDetailModelSerializer(serializers.ModelSerializer):
    """Profile detail model serializer."""
    
    class Meta:
        """Meta options."""
        model = ProfileDetail
        fields = (
            'work', 'education', 'current_city',
            'web_site', 'social_links'
        )


class ProfileModelSerializer(serializers.ModelSerializer):
    """Profile model serializer."""

    details = ProfileDetailModelSerializer(read_only=True)

    class Meta:
        """Meta options."""
        model = Profile
        fields = (
            'photo',
            'cover_photo',
            'about',
            'datails',
            'hobby',
            'birth_date',
            'origin_country'
        )
        read_only_fields = ['details']