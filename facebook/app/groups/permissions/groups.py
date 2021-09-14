"""Groups permissions."""

# Django REST Framework
from rest_framework.permissions import BasePermission

# Models
from groups.models import Membership


class IsGroupAdmin(BasePermission):
    """Allow access only to group admin."""

    def has_object_permission(self, request, view, obj):
        """Check requesting user and group admin are the same."""
        try:
            Membership.objects.get(
                user=request.user, group=obj,
                is_admin=True, is_active=True)
        except Membership.DoesNotExist:
            return False
        return True
