from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import MediaContent
from .serializers import MediaContentSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

class MediaContentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows media content to be viewed or edited.
    """
    queryset = MediaContent.objects.all()
    serializer_class = MediaContentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'title']