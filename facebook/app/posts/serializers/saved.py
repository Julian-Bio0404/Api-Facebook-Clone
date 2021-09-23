"""Saved serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from app.posts.models import Saved, CategorySaved

# Serializers
from app.posts.serializers import PostModelSerializer


class CategorySavedModelSerializer(serializers.ModelSerializer):
    """Category saved model serializer."""
    
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        """Meta options."""
        model = CategorySaved
        fields = ['user', 'name']
        read_only_fields = ['user']

    def create(self, data):
        """Create category."""
        return CategorySaved.objects.create(**data, user=self.context['user'])


class SavedPostModelSerializer(serializers.ModelSerializer):
    """Saved post model serializer."""

    user = serializers.StringRelatedField(read_only=True)
    post = PostModelSerializer(read_only=True)
    saved_category = serializers.StringRelatedField()

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

    def create(self, data):
        """Create saved."""
        saved = Saved.objects.create(
            user=self.context['user'], 
            post=self.context['post'], 
            saved_category=self.context['saved_category'])
        return saved
