"""Posts serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from posts.models import Comment

# Serializers
from users.serializers import UserModelSummarySerializer


class CommentModelSerializer(serializers.ModelSerializer):
    """Post model serializer."""

    user = UserModelSummarySerializer(read_only=True)

    class Meta:
        """Meta options."""
        model = Comment
        fields = ['user', 'text', 'reactions']

        read_only_fields = [
            'user', 'reactions'
        ]

    def create(self, data):
        """Create a post."""
        user = self.context['user']
        profile = user.profile
        post = self.context['post']
        comment = Comment.objects.create(
            **data, 
            user=user, 
            profile=profile, 
            post=post
        )
        comment.save()
        return comment
