"""Reactions serializers."""

# Django REST Framework
from rest_framework import serializers

# Serializers
from users.serializers import UserModelSummarySerializer
from posts.serializers.comments import CommentModelSerializer
from posts.serializers.posts import PostModelSerializer

# Models
from posts.models import ReactionComment, ReactionPost


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

    def validate(self, data):
        """Velidate.
        verify that the user's reaction does not exist yet
        """
        try:
            user = self.context['user']
            reaction = ReactionPost.objects.get(
                user=user
            )
            # Si la reaccion del usuario existe, esta se elimina
            reaction.delete()
            post = self.context['post']
            post.reactions -= 1
            post.save()
        except ReactionPost.DoesNotExist:
            # Si no existe, procede a crearse
            return data

    def create(self, data):
        """Create a reaction post."""
        # Reaction post
        user = self.context['user']
        post = self.context['post']
        reaction_post = ReactionPost.objects.create(
            **data,
            user=user,
            profile=user.profile,
            post=post
        )
        reaction_post.save()

        # Post
        post.reactions += 1
        post.save()
        return reaction_post


class ReactionPostModelSummarySerializer(ReactionPostModelSerializer):
    """Reaction post model summary serializer"""

    class Meta:
        """Meta options."""
        model = ReactionPost
        fields = [
            'user', 'reaction'
        ]

        read_only_fields = [
            'user', 'post'
        ]


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
        comment = self.context['comment']
        reaction_comment = ReactionComment.objects.create(
            **data, 
            user=user, 
            profile= user.profile, 
            comment=comment
        )
        reaction_comment.save()
        return reaction_comment
        