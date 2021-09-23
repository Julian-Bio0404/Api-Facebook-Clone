"""Profile serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from app.users.models import Profile, ProfileDetail


class ProfileDetailModelSerializer(serializers.ModelSerializer):
    """Profile detail model serializer."""
    
    class Meta:
        """Meta options."""
        model = ProfileDetail
        fields = [
            'work', 'education', 'current_city',
            'web_site', 'social_links'
        ]


class ProfileModelSerializer(serializers.ModelSerializer):
    """Profile model serializer."""

    profiledetail = ProfileDetailModelSerializer(read_only=True)

    class Meta:
        """Meta options."""
        model = Profile
        fields = [
            'photo', 'cover_photo',
            'about', 'hobby',
            'birth_date', 'origin_country',
            'profiledetail'
        ]

        read_only_fields = [
            'profiledetail'
        ]
        

class ProfileModelSummarySerializer(ProfileModelSerializer):
    """Profile model data summary serializer."""

    class Meta:
        """Meta options."""
        model = Profile
        fields = [
            'photo', 'origin_country'
        ]
