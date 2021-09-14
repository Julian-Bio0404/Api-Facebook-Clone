"""Memberships permissions."""

# Django REST Framework
from rest_framework.permissions import BasePermission

# Models
from groups.models import Invitation, Membership


class IsGroupMember(BasePermission):
    """Allow access only to group members.
    Expect that the views implementing this permission
    have a `group` attribute assigned.
    """

    def has_permission(self, request, view):
        """Check user is an active member of the group."""
        try:
            Membership.objects.get(
                user=request.user,
                group=view.group,
                is_active=True)
        except Membership.DoesNotExist:
            return False
        return True


class IsSelfUserInvited(BasePermission):
    """Allow access only to user invited."""
    
    def has_permission(self, request, view):
        """Check requesting user and 
        user invited are the same.
        """
        try:
            Invitation.objects.get(
                used_by=request.user, 
                group=view.group, used=False)
        except Invitation.DoesNotExist:
            return False
        return True


class IsMembershipAdmin(BasePermission):
    """Allow access only to group admin."""

    def has_permission(self, request, view):
        """Check requesting user and group admin are the same."""
        try:
            Membership.objects.get(
                user=request.user, group=view.group,
                is_admin=True, is_active=True)
        except Membership.DoesNotExist:
            return False
        return True


class IsSelfUserInvitedOrAdmin(BasePermission):
    """Allow access only to 
    group  admin or to user invited.
    """
    
    def has_object_permission(self, request, view, obj):
        """Check requesting user and group admin are the same
        or reqeusting user is user invited."""
        try:
            Membership.objects.get(
                user=request.user, group=view.group,
                is_admin=True, is_active=True)
        except Membership.DoesNotExist:
            return request.user == obj.user
        return True

