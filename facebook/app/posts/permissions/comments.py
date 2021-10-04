"""Comment permissions."""

# Django REST Framework
from rest_framework.permissions import BasePermission


class IsCommentOwner(BasePermission):
    """Allow access only to post owner."""

    def has_object_permission(self, request, view, obj):
        """Check requesting user and comment owner are the same."""
        return request.user == obj.user


class IsCommentOrPostOwner(BasePermission):
    """Allow access only to comment or post owner."""

    def has_object_permission(self, request, view, obj):
        """Check requesting user is comment owner or post owner."""
        if request.user == obj.user or request.user == obj.post.user:
            return True
        else:
            return False


class IsFriendPostOwner(BasePermission):
    """Allow access only to friends of the post owner."""

    def has_object_permission(self, request, view, obj):
        """Check privacy obj and if user is friend of the post owner. """
        post_owner = obj.post.user
        friends = post_owner.profile.friends.all()
        
        if obj.post.privacy == 'PUBLIC':
            return True
        elif obj.post.privacy == 'FRIENDS':
            if request.user in friends or request.user == post_owner:
                return True
            else:
                return False
        elif obj.post.privacy == 'SPECIFIC_FRIENDS':
            if request.user in obj.post.specific_friends.all() or request.user == post_owner:
                return True
            else:
                return False
        elif obj.post.privacy == 'FRIENDS_EXC':
            if request.user in obj.post.friends_exc.all():
                return False
            else: 
                return True

