"""Users model admin."""

# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Models
from users.models import User, Profile, ProfileDetail


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """User model admin."""

    list_display = [
        'first_name', 'last_name',
        'email', 'username', 
        'phone_number', 'is_verified',
        'created'
    ]

    search_fields = [
        'username', 'email', 
        'first_name', 'last_name'
    ]

    list_filter = ['is_verified']
    ordering = ['first_name', 'last_name']


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Profile model admin."""

    list_display = [
        'user', 'hobby', 
        'birth_date', 'origin_country'
    ]

    search_fields = [
        'user__username', 'user__email', 
        'user__first_name', 'user__last_name'
    ]

    list_filter = ['origin_country']
    ordering = ['user__first_name', 'user__las_name']


@admin.register(ProfileDetail)
class ProfileDetailAdmin(admin.ModelAdmin):
    """Profile Detail model admin."""

    list_display = [
        'user', 'work',
        'education', 'current_city',
        'web_site', 'social_links'
    ]

    search_fields = ['current_city']
    ordering = ['user__first_name', 'user__las_name']