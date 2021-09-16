"""Saved permissions."""

# Django REST Framework
from rest_framework.permissions import BasePermission


class IsSavedOwner(BasePermission):
    """Allow access only to saved owner."""

    def has_object_permission(self, request, view, obj):
        """Check requesting user and saved owner are the same."""
        return request.user == obj.user