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
            'video', 'privacy', 'feeling',
            'location', 'tag_friends',
            'reactions', 'destination'
        ]

        read_only_fields = [
            'user', 'reactions'
        ]

    def validate(self, data):
        """Verify that about, picture or video are present."""
        media = ['picture', 'video', 'about']
        match = False
        for i in media:
            if i in data:
                match = True
                break
        if match == False:
            raise serializers.ValidationError(
                'You must include an about, picture or video.')
        return data

    def create(self, data):
        """Create a post."""
        user = self.context['user']
        profile = user.profile
        post = Post.objects.create(**data, user=user, profile=profile)
        post.save()
        return post
