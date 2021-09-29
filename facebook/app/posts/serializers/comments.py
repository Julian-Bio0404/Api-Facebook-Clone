"""Comment serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from app.posts.models import Comment

# Tasks
from taskapp.tasks.notifications import create_notification


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
            **data, user=user, profile=profile, post=post)

        # Post
        post.comments += 1
        post.save()
        if user != post.user:
            type = 'Comment Post'
            create_notification.delay(
                comment.user.pk, post.user.pk, type, comment.post.pk, comment.pk)
        return comment
