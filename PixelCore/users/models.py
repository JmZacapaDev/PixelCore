from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.

    Fields:
    - user_id: Unique identifier for the user (UUID).
    - username: User's chosen username (unique, optional).
    - email: User's email address (unique, used for authentication).
    - rating_count: Number of ratings given by the user.
    - created_at: Timestamp when the user account was created.
    - password: Hashed password (inherited from AbstractUser).
    - is_active: Boolean flag indicating if the user account is active (inherited from AbstractUser).
    - is_staff: Boolean flag indicating if the user can access the admin site (inherited from AbstractUser).
    - is_superuser: Boolean flag indicating if the user has all permissions without explicitly assigning them (inherited from AbstractUser).
    """
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # Make username unique and optional
    username = models.CharField(max_length=150, unique=True, null=True, blank=True)
    email = models.EmailField(unique=True)
    rating_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    # No required fields other than email, which is the USERNAME_FIELD.
    # AbstractUser already provides password, is_active, is_staff, is_superuser.
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["-created_at"]