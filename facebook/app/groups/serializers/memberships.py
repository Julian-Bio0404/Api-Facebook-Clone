"""Membership serializer."""

# Django REST Framework
from rest_framework import serializers

# Models
from app.groups.models import Membership, Invitation

# Serializers
from app.users.serializers import UserModelSerializer


class MembershipModelSerializer(serializers.ModelSerializer):
    """Membership model serializer."""

    user = UserModelSerializer(read_only=True)
    invited_by = serializers.StringRelatedField()
    invited_at = serializers.DateTimeField(source='created', read_only=True)

    class Meta:
        """Meta options."""
        model = Membership
        fields = [
            'user', 'is_admin',
            'invited_by', 'invited_at'
        ]

        read_only_fields = [
            'user', 'invited_at', 
            'is_admin'
        ]


class AddMemberSerializer(serializers.Serializer):
    """
    Add member serializer.
    Handle the addition of a new member to a group.
    """

    invitation_code = serializers.CharField(min_length=8)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate_user(self, data):
        """Verify user is not already a member."""
        group = self.context['group']
        user = data
        membership = Membership.objects.filter(group=group, user=user)

        if membership.exists():
            raise serializers.ValidationError(
                'User has already been invited to this group.')
        return data

    def validate_invitation_code(self, data):
        """Verify code exists and that it is related to the group."""
        try:
            invitation = Invitation.objects.get(
                code=data, group=self.context['group'], used=True)
        except Invitation.DoesNotExist:
            raise serializers.ValidationError('Invalid invitation code.')
        self.context['invitation'] = invitation
        return data

    def create(self, data):
        """Create new group's membership."""
        group = self.context['group']
        invitation = self.context['invitation']
        user = self.context['user']

        # Member creation
        member = Membership.objects.create(
            user=user,
            profile=user.profile,
            group=group,
            invited_by=invitation.sent_by)
        return member
