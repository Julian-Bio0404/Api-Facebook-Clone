"""Friend's Request serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from users.models import FriendRequest, User

# Serializers
from users.serializers import UserModelSummarySerializer


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
    
    def create(self, data):
        """Create a friend's request."""
        friend_request = FriendRequest.objects.create(
            requesting_user=self.context['requesting_user'], 
            requested_user=self.context['requested_user']
        )
        friend_request.save()
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
        friend_request = self.context['friend_request']
        friend_request.accepted = True
        friend_request.save()