"""Comment serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from app.posts.models import Comment


class CommentModelSerializer(serializers.ModelSerializer):
    """Post model serializer."""

    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        """Meta options."""
        model = Comment
        fields = ['user', 'text', 'reactions']

        read_only_fields = [
            'user', 'reactions'
        ]

    def create(self, data):
        """Create a comment."""
        # comment
        user = self.context['user']
        profile = user.profile
        post = self.context['post']
        comment = Comment.objects.create(
            **data, user=user, 
            profile=profile, 
            post=post)
        comment.save()

        # Post
        post.comments += 1
        post.save()
        return comment
