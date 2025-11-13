from rest_framework import serializers
from .models import Rating

class RatingSerializer(serializers.ModelSerializer):
    """
    Serializer for the Rating model.
    """
    user = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Rating
        fields = ('rating_id', 'user', 'media_content', 'value', 'created_at')
        read_only_fields = ('rating_id', 'created_at')
