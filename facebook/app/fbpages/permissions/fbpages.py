"""Fbpages permissions."""

# Django REST Framework
from rest_framework.permissions import BasePermission


class IsCreatorPage(BasePermission):
    """Allow access only to page admin."""

    def has_object_permission(self, request, view, obj):
        """Check requesting user is creator of the page."""
        return request.user == obj.creator


class IsCreatorOrAdminPage(BasePermission):
    """Allow access only to page admin or creator."""

    def has_object_permission(self, request, view, obj):
        """Check requesting user is admin or creator of the page."""
        if request.user == obj.creator or request.user in obj.admins.all():
            return True
        else: 
            return False
        
