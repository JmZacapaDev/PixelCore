from django.contrib import admin
from .models import MediaContent

@admin.register(MediaContent)
class MediaContentAdmin(admin.ModelAdmin):
    """
    Admin configuration for the MediaContent model.
    """
    list_display = ('title', 'category', 'content_url', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)