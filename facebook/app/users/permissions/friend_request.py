"""Friend request permissions."""

# Django REST Framework
from rest_framework.permissions import BasePermission


class IsRequestedUser(BasePermission):
    """Allow access only to objects
    owned by the requesting user.
    """

    def has_object_permission(self, request, view, obj):
        """Check obj and user are the same. """
        return request.user == obj.requested_user