"""Pages model admin."""

# Django
from django.contrib import admin

# Models
from fbpages.models import Category, Page, PageDetail


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Category model admin."""

    list_display = [
        'pk','name'
    ]


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    """Page model admin."""

    list_display = [
        'name', 'slug_name', 
        'creator', 'about',
        'category', 'likes'
    ]

    search_fields = ['name']
    list_filter = ['category']


@admin.register(PageDetail)
class PageDetail(admin.ModelAdmin):
    """Page detail model admin."""

    list_display = [
        'page', 'direction', 
        'phone_number', 'web_site',
        'social_links'
    ]

    search_fields = ['page']
    list_filter = ['page__category']
