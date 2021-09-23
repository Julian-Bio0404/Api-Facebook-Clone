"""Fbpages serializers."""

# Django REST Framework
from rest_framework import serializers

# Model
from app.fbpages.models import Category, Page, PageDetail


class PageDetailModelSerializers(serializers.ModelSerializer):
    """Page detail model serializer."""
    
    class Meta:
        """Meta options."""
        model = PageDetail
        fields = [
            'direction', 'phone_number', 
            'web_site', 'social_links'
        ]


class PageModelSerializer(serializers.ModelSerializer):
    """Page model serializer."""
    
    creator = serializers.StringRelatedField(read_only=True)
    category = serializers.StringRelatedField(read_only=True)
    pagedetail = PageDetailModelSerializers(read_only=True)

    class Meta:
        """Meta options."""
        model = Page
        fields = [
           'name', 'slug_name', 'creator',
           'photo', 'cover_photo', 'about',
           'pagedetail', 'category', 'likes'
        ]

        read_only_fields = [
            'creator', 'pagedetail',
            'category', 'likes'
        ]

    def create(self, data):
        """Create a page."""
        creator = self.context['creator']

        try:
            category = Category.objects.get(name=self.context['category'])
        except Category.DoesNotExist:
            raise serializers.ValidationError('The category does not exist.')
        page = Page.objects.create(**data, creator=creator, category=category)
        PageDetail.objects.create(page=page)
        return page
