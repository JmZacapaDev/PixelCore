from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Custom Admin for the User model.
    Extends Django's default UserAdmin to include custom fields.
    """
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('user_id', 'rating_count')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('user_id', 'rating_count')}),
    )
    list_display = ('email', 'username', 'rating_count', 'is_staff', 'is_active')
    search_fields = ('email', 'username')
    ordering = ('email',)