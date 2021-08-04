"""Posts model admin."""

# Django
from django.contrib import admin

# Models
from posts.models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Post model admin."""

    list_display = [
        'pk','user', 'about', 'privacy', 
        'feeling', 'location', 'tag_friends', 
        'reactions', 'group', 'created'
    ]

    search_fields = [
        'user__username', 'location', 'privacy',
        'group'
    ]

    list_filter = [
        'user__username', 'location', 'privacy',
        'group'
    ]

    ordering = ['-created']