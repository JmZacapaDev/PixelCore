from django.db import models
import uuid
from users.models import User
from content.models import MediaContent

class Rating(models.Model):
    """
    Rating model to store user ratings for media content.

    Fields:
    - rating_id: Unique identifier for the rating (UUID).
    - user: Foreign key to the User model, indicating who made the rating.
    - media_content: Foreign key to the MediaContent model, indicating what was rated.
    - value: Integer value of the rating (1 to 5).
    - created_at: Timestamp when the rating was created.
    """
    RATING_CHOICES = [
        (1, '1 - Poor'),
        (2, '2 - Fair'),
        (3, '3 - Good'),
        (4, '4 - Very Good'),
        (5, '5 - Excellent'),
    ]

    rating_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    media_content = models.ForeignKey(MediaContent, on_delete=models.CASCADE, related_name='ratings')
    value = models.IntegerField(choices=RATING_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Rating"
        verbose_name_plural = "Ratings"
        # Ensure a user can only rate a specific media content once
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.email} rated {self.media_content.title} as {self.value}"