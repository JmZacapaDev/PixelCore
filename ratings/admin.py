from django.contrib import admin
from .models import Rating

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Rating model.
    """
    list_display = ('user', 'media_content', 'value', 'created_at')
    list_filter = ('value', 'created_at')
    search_fields = ('user__email', 'media_content__title')
    ordering = ('-created_at',)