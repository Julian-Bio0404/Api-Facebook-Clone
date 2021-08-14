"""Reactions serializers."""

# Django REST Framework
from rest_framework import serializers

# Serializers
from users.serializers import UserModelSummarySerializer
from posts.serializers import CommentModelSerializer

# Models
from posts.models import ReactionComment, ReactionPost
from posts.serializers import PostModelSerializer


class ReactionPostModelSerializer(serializers.ModelSerializer):
    """Reaction post model serializer."""

    user = UserModelSummarySerializer(read_only=True)
    post = PostModelSerializer(read_only=True)

    class Meta:
        """Meta options."""
        model = ReactionPost
        fields = [
            'user', 'post', 'reaction'
        ]

        read_only_fields = [
            'user', 'post'
        ]

    def create(self, data):
        """Create a reaction post."""
        user = self.context['user']
        profile = user.profile
        post = self.context['post']
        reaction_post = ReactionPost.objects.create(
            **data, 
            user=user, 
            profile=profile, 
            post=post
        )
        reaction_post.save()
        return reaction_post


class ReactionCommentModelSerializer(serializers.ModelSerializer):
    """Reaction comment model serializer."""

    user = UserModelSummarySerializer(read_only=True)
    comment = CommentModelSerializer(read_only=True)

    class Meta:
        """Meta options."""
        model = ReactionComment
        fields = [
            'user', 'comment', 'reaction'
        ]

        read_only_fields = [
            'user', 'comment'
        ]

    def create(self, data):
        """Create a reaction comment."""
        user = self.context['user']
        profile = user.profile
        comment = self.context['comment']
        reaction_comment = ReactionComment.objects.create(
            **data, 
            user=user, 
            profile=profile, 
            comment=comment
        )
        reaction_comment.save()
        return reaction_comment
        