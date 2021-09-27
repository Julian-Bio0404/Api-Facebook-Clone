"""Chat models admin."""

# Django
from django.contrib import admin

# Models
from app.chats.models import Message, Thread


class MessageInline(admin.StackedInline):
    """Message stacked inline admin."""
    
    model = Message
    fields = ('sender', 'text')
    readonly_fields = ('sender', 'text')


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    """Thread model admin."""

    model = Thread
    inlines = (MessageInline,)

