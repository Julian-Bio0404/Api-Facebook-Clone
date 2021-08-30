"""Fbpages serializers."""

# Django REST Framework
from rest_framework import serializers

# Model
from fbpages.models import Page, Category


class PageModelSerializer(serializers.ModelSerializer):
    """Page model serializer."""
    
    creator = serializers.StringRelatedField()
    category = serializers.StringRelatedField()

    class Meta:
        """Meta options."""
        model = Page
        fields = [
           'name', 'slug_name', 'creator',
           'photo', 'cover_photo', 'about',
           'category', 'likes'
        ]

        read_only_fields = [
            'creator', 'category',
            'likes'
        ]

    def create(self, data):
        """Create a page."""
        creator = self.context['creator']
        try:
            category = Category.objects.get(name=self.context['category'])
        except Category.DoesNotExist:
            raise serializers.ValidationError('The category does not exist.')
        page = Page.objects.create(**data, creator=creator, category=category)
        page.save()
        return page
