"""Post permissions."""

# Django REST Framework
from rest_framework.permissions import BasePermission


class IsPostOwner(BasePermission):
    """Allow access only to post owner."""

    def has_object_permission(self, request, view, obj):
        """Check requesting user and post owner are the same."""
        return request.user == obj.user


class IsFriend(BasePermission):
    """Allow access only to friends of a user."""

    def has_object_permission(self, request, view, obj):
        """Check privacy obj and if user is friend of the post owner. """
        post_owner = obj.user
        friends = post_owner.profile.friends.all()
        
        if obj.privacy == 'PUBLIC':
            return True
        else:
            if request.user in friends or request.user == post_owner:
                return True
            else:
                return False