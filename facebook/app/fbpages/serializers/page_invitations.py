"""Pages Invitation serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from fbpages.models import PageInvitation
from users.models import User


class PageInvitationSerializer(serializers.ModelSerializer):
    """Page invitation model serializer."""
    
    inviting_user = serializers.StringRelatedField(read_only=True)
    guest_user = serializers.StringRelatedField()
    page = serializers.StringRelatedField(read_only=True)

    class Meta:
        """Meta options."""
        model = PageInvitation
        fields = [
            'inviting_user', 'guest_user', 
            'page', 'used'
        ]

        read_only_fields = ['inviting_user', 'page', 'used']


class CreatePageInvitation(serializers.Serializer):
    """Create Page invitation."""

    inviting_user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    guest_user = serializers.CharField()

    def validate_guest_user(self, data):
        """Check that guest user exists and that the invitation 
        does not yet exist or that the user is not a follower of the page.
        """
        try:
            user = User.objects.get(username=data)
        except User.DoesNotExist:
            raise serializers.ValidationError(f'The user with username {data} does not exists.')

        page = self.context['page']
        invitation = PageInvitation.objects.filter(guest_user=user, page=page)
        if invitation.exists():
            raise serializers.ValidationError(
                'User has already been invited to this page.')
        if user in page.page_followers.all():
            raise serializers.ValidationError(
                'The user already likes this page.')
        self.context['user'] = user
        return data
    
    def create(self, validated_data):
        validated_data.pop('guest_user')
        invitation = PageInvitation.objects.create(
            **validated_data, 
            guest_user=self.context['user'], page=self.context['page'])
        return invitation