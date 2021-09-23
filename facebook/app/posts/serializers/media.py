"""Picture and Video serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from app.posts.models import Picture, Video


class ImageModelSerializer(serializers.ModelSerializer):
    """Image model serializer."""

    content = serializers.ImageField(max_length=1000)

    class Meta:
        """Meta options."""
        model = Picture
        fields = ['content']


class VideoModelSerializer(serializers.ModelSerializer):
    """Video model serializer."""

    content = serializers.FileField(max_length=1000)

    class Meta:
        """Meta options."""
        model = Video
        fields = ['content']