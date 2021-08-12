"""Posts model admin."""

# Django
from django.contrib import admin

# Models
from posts.models import Comment, Post, ReactionComment, ReactionPost


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Post model admin."""

    list_display = [
        'pk','user', 'destination','about', 'privacy', 
        'feeling', 'location', 'tag_friends', 
        'reactions', 'created'
    ]

    search_fields = [
        'user__username', 'destination', 
        'location', 'privacy'
    ]

    list_filter = [
        'user__username', 'destination', 
        'location', 'privacy'
    ]

    ordering = ['-created']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Comment model admin."""

    list_display = [
        'pk', 'user', 'post', 'text'
    ]

    search_fields = [
        'user__username', 'post'
    ]

    list_filter = [
        'user__username', 'post'
    ]


@admin.register(ReactionPost)
class ReactionPostAdmin(admin.ModelAdmin):
    """Reaction post model admin."""

    list_display = [
        'pk', 'user', 'post', 'reaction'
    ]

    list_filter = ['post']


@admin.register(ReactionComment)
class ReactionCommentAdmin(admin.ModelAdmin):
    """Reaction comment model admin."""

    list_display = [
        'pk', 'user', 'comment', 'reaction'
    ]

    list_filter = ['comment']
