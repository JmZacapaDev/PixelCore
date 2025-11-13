from rest_framework import serializers
from .models import MediaContent

class MediaContentSerializer(serializers.ModelSerializer):
    """
    Serializer for the MediaContent model.
    """
    class Meta:
        model = MediaContent
        fields = '__all__'
        read_only_fields = ('media_id', 'created_at')
