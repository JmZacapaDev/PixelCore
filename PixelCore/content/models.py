from django.db import models
import uuid

class MediaContent(models.Model):
    """
    MediaContent model to store information about various types of content.

    Fields:
    - media_id: Unique identifier for the media content (UUID).
    - title: Title of the media content.
    - description: Detailed description of the media content.
    - category: Category of the content (e.g., game, video, artwork, music).
    - thumbnail_url: URL for a thumbnail image (optional). (TODO: Integrate with object storage bucket like S3)
    - content_url: URL for the actual media content. (TODO: Integrate with object storage bucket like S3)
    - created_at: Timestamp when the media content was added.
    """
    CATEGORY_CHOICES = [
        ('game', 'Game'),
        ('video', 'Video'),
        ('artwork', 'Artwork'),
        ('music', 'Music'),
    ]

    media_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    thumbnail_url = models.URLField(max_length=200, blank=True, null=True)
    content_url = models.URLField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Media Content"
        verbose_name_plural = "Media Content"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title