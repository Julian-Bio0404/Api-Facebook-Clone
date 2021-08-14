"""Posts serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from posts.models import Post

# Serializers
from users.serializers import UserModelSummarySerializer


class PostModelSerializer(serializers.ModelSerializer):
    """Post model serializer."""

    user = UserModelSummarySerializer(read_only=True)

    class Meta:
        """Meta options."""
        model = Post
        fields = [
            'user','about', 'picture',
            'privacy', 'feeling',
            'location', 'tag_friends',
            'reactions', 'destination'
        ]

        read_only_fields = [
            'user', 'reactions'
        ]

    def create(self, data):
        """Create a post."""
        user = self.context['user']
        profile = user.profile
        post = Post.objects.create(**data, user=user, profile=profile)
        post.save()
        return post
