"""Profile permissions."""

# Django REST Framework
from rest_framework.permissions import BasePermission


class IsProfileOwner(BasePermission):
    """Allow access only to objects
    owned by the requesting user.
    """

    def has_object_permission(self, request, view, obj):
        """Check obj and profile are the same. """
        return request.user.profile == obj