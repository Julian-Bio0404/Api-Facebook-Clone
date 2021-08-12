"""Posts serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from posts.models import Post

# Serializers
from users.serializers import ProfileModelSerializer, UserModelSerializer


class PostModelSerializer(serializers.ModelSerializer):
    """Post model serializer."""

    user = UserModelSerializer(read_only=True)
    profile = ProfileModelSerializer(read_only=True)

    class Meta:
        """Meta options."""
        model = Post
        fields = ['__all__']
        read_only_fields = [
            'user', 'profile', 'reactions'
        ]