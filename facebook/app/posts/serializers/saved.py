"""Saved serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from posts.models import Saved, CategorySaved

# Serializers
from posts.serializers import PostModelSerializer


class CategorySavedModelSerializer(serializers.ModelSerializer):
    """Category saved model serializer."""
    
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        """Meta options."""
        model = CategorySaved
        fields = ['user', 'name']
        read_only_fields = ['user']


class SavedPostModelSerializer(serializers.ModelSerializer):
    """Saved post model serializer."""

    user = serializers.StringRelatedField(read_only=True)
    post = PostModelSerializer(read_only=True)

    class Meta:
        """Meta options."""
        model = Saved
        fields = [
            'user','post', 
            'saved_category'
        ]

        read_only_fields = [
            'user', 'post',
            'saved_category'
        ]
