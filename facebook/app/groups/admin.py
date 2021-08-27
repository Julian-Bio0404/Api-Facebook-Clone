"""Groups model admin."""

# Django
from django.contrib import admin

# Models
from groups.models import Group, Membership, Invitation


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    """Group model admin."""

    list_display = [
        'pk','name', 'slug_name',
        'about', 'is_public'
    ]

    search_fields = ['name', 'slug_name']
    list_filter = ['is_public']


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    """Membership model admin."""

    list_display = [
        'user', 'group', 
        'is_admin', 'invited_by'
    ]

    search_fields = ['user', 'group']
    list_filter = ['group']


@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    """Invitation model admin."""
    
    list_display = [
        'sent_by', 'used_by', 
        'group', 'code', 
        'used', 'used_at'
    ]