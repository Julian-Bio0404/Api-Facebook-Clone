"""Posts model admin."""

# Django
from django.contrib import admin

# Models
from posts.models import (CategorySaved,
                          Comment, Post,
                          ReactionComment,
                          ReactionPost,
                          Saved, Shared)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Post model admin."""

    list_display = [
        'pk','user', 'destination',
        'name_destination','about', 
        'privacy', 'feeling', 'location', 
        'reactions', 'comments', 
        're_post', 'created'
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
        'pk', 'user', 'post', 
        'text', 'reactions'
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


@admin.register(Shared)
class SharedAdmin(admin.ModelAdmin):
    """Shared model admin."""

    list_display = [
        'user', 'about', 'post'
    ]

    list_filter = ['post']


@admin.register(CategorySaved)
class CategorySavedAdmin(admin.ModelAdmin):
    """Category Saved model admin."""

    list_display = [
        'user', 'name'
    ]


@admin.register(Saved)
class SavedAdmin(admin.ModelAdmin):
    """Saved model admin."""

    list_display = [
        'user', 'post'
    ]

    list_filter = ['user']
