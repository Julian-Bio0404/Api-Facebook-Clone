"""Groups model admin."""

# Django
from django.contrib import admin

# Models
from groups.models import Group


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    """Group model admin."""

    list_display = [
        'pk','name', 'slug_name',
        'about', 'is_public'
    ]

    search_fields = ['name', 'slug_name']

    list_filter = ['is_public']
    