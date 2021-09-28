"""Friend's Request serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from app.users.models import FriendRequest

# Serializers
from .users import UserModelSummarySerializer

# Tasks
from taskapp.tasks.notifications import create_notification


class FriendRequestModelSerializer(serializers.ModelSerializer):
    """Friend request model serializer."""
    
    requesting_user = UserModelSummarySerializer(read_only=True)
    requested_user = UserModelSummarySerializer(read_only=True)

    class Meta:
        """Meta options."""
        model = FriendRequest
        fields = [
            'requesting_user', 
            'requested_user',
            'accepted'
        ]

        read_only_fields = [
            'requesting_user', 
            'requested_user',
            'accepted'
        ]
    
    def validate(self, data):
        """Verify friend request """
        requesting_user = self.context['requesting_user']
        requested_user = self.context['requested_user']

        if requesting_user == requested_user:
            raise serializers.ValidationError(
                "You can't send friend request to yourself.")

        if requesting_user.profile in requested_user.friends.all():
            raise serializers.ValidationError(
                f'You are already a friend of {requested_user.username}.')
        try:
            friend_request = FriendRequest.objects.get(
                requesting_user=requesting_user, 
                requested_user=requested_user)

            if friend_request:
                raise serializers.ValidationError(
                    'You already sent a friend request.')
        except FriendRequest.DoesNotExist:
            try:
                friend_request2 = FriendRequest.objects.get(
                    requesting_user=requested_user,
                    requested_user=requesting_user)
                if friend_request2:
                    raise serializers.ValidationError(
                        'You already sent a friend request.')
            except FriendRequest.DoesNotExist:
                return data

    def create(self, data):
        """Create a friend's request."""
        requesting_user = self.context['requesting_user']
        requested_user = self.context['requested_user']
        friend_request = FriendRequest.objects.create(
            requesting_user=requesting_user, 
            requested_user=requested_user)

        type = 'Friend Request'
        create_notification.delay(
            requesting_user.pk, requested_user.pk, type, friend_request.pk)
        return friend_request


class AcceptFriendRequestSerializer(serializers.Serializer):
    """Accept friend's request serializer."""

    accepted = serializers.BooleanField()

    def validate(self, data):
        """Check accepted field."""
        if data['accepted'] != True:
            raise serializers.ValidationError('Friend request not accepted.')
        return data
            
    def save(self):
        """Accept friend request."""
        # Friend request
        friend_request = self.context['friend_request']
        friend_request.accepted = True
        friend_request.save()

        # Update user's profile
        requesting_user = friend_request.requesting_user
        requested_user = friend_request.requested_user

        requesting_user.profile.friends.add(requested_user)
        requested_user.profile.friends.add(requesting_user)

        requesting_user.profile.save()
        requested_user.profile.save()

        type = 'Friend Accept'
        create_notification.delay(
            requested_user.pk, requesting_user.pk, type, friend_request.pk)
