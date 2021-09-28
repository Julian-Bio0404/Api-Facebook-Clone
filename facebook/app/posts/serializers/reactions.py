"""Reactions serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from app.posts.models import ReactionComment, ReactionPost

# Serializers
from app.posts.serializers import CommentModelSerializer, PostModelSerializer
from app.users.serializers import UserModelSummarySerializer

# Tasks
from taskapp.tasks.notifications import create_notification


class ReactionPostModelSerializer(serializers.ModelSerializer):
    """Reaction post model serializer."""

    user = serializers.StringRelatedField(read_only=True)
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
        """verify that the user's reaction does not exist yet."""
        try:
            user = self.context['user']
            reaction = ReactionPost.objects.get(user=user)

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
            **data, user=user, profile=user.profile, post=post)
        reaction_post.save()

        # Post
        post.reactions += 1
        post.save()

        if user != post.user:
            type = 'Reaction Post'
            create_notification.delay(
                reaction_post.user.pk, post.user.pk, type, post.pk)
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

    def validate(self, data):
        """Verify that the user's reaction does not exist yet."""
        try:
            user = self.context['user']
            reaction = ReactionComment.objects.get(
                user=user
            )
            # Si la reaccion del usuario existe, esta se elimina
            reaction.delete()
            comment = self.context['comment']
            comment.reactions -= 1
            comment.save()
        except ReactionComment.DoesNotExist:
            # Si no existe, procede a crearse
            return data

    def create(self, data):
        """Create a reaction comment."""
        # Reaction comment
        user = self.context['user']
        comment = self.context['comment']
        reaction_comment = ReactionComment.objects.create(
            **data, user=user, profile=user.profile, comment=comment)
        reaction_comment.save()

        # Comment
        comment.reactions += 1
        comment.save()
        if user != comment.user:
            type = 'Reaction Comment'
            create_notification.delay(
                reaction_comment.user.pk, comment.user.pk, type, comment.pk)
        return reaction_comment


class ReactionCommentModelSummarySerializer(ReactionCommentModelSerializer):
    """Reaction comment model summary serializer"""

    class Meta:
        """Meta options."""
        model = ReactionComment
        fields = [
            'user', 'reaction'
        ]

        read_only_fields = [
            'user', 'comment'
        ]
