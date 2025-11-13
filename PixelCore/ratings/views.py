import rest_framework
from django.db import IntegrityError
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Rating
from .serializers import RatingSerializer
from .permissions import IsOwnerOrReadOnly # Import custom permission
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample

class RatingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows ratings to be viewed, created, updated or deleted.
    """
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly] # Add custom permission

    def perform_create(self, serializer):
        try:
            serializer.save(user=self.request.user)
        except IntegrityError:
            raise rest_framework.serializers.ValidationError({"detail": "You have already rated this media content."})

    @extend_schema(
        summary="List all ratings or filter by media content",
        parameters=[
            OpenApiParameter(
                name='media_content_id',
                type={'type': 'string', 'format': 'uuid'},
                location=OpenApiParameter.QUERY,
                description='Filter ratings by media content ID',
                required=False
            ),
        ],
        responses={
            200: RatingSerializer(many=True),
        }
    )
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        media_content_id = request.query_params.get('media_content_id')
        if media_content_id:
            queryset = queryset.filter(media_content__media_id=media_content_id)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Retrieve a specific rating",
        responses={
            200: RatingSerializer,
            404: OpenApiExample(
                'Not Found',
                value={'detail': 'Not found.'},
                response_only=True,
                media_type='application/json',
            ),
        }
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Create a new rating",
        request=RatingSerializer,
        responses={
            201: RatingSerializer,
            400: OpenApiExample(
                'Bad Request',
                value={'value': ['"1" is not a valid choice.']},
                response_only=True,
                media_type='application/json',
            ),
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="Update an existing rating",
        request=RatingSerializer,
        responses={
            200: RatingSerializer,
            400: OpenApiExample(
                'Bad Request',
                value={'value': ['"1" is not a valid choice.']},
                response_only=True,
                media_type='application/json',
            ),
            404: OpenApiExample(
                'Not Found',
                value={'detail': 'Not found.'},
                response_only=True,
                media_type='application/json',
            ),
        }
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary="Partially update an existing rating",
        request=RatingSerializer,
        responses={
            200: RatingSerializer,
            400: OpenApiExample(
                'Bad Request',
                value={'value': ['"1" is not a valid choice.']},
                response_only=True,
                media_type='application/json',
            ),
            404: OpenApiExample(
                'Not Found',
                value={'detail': 'Not found.'},
                response_only=True,
                media_type='application/json',
            ),
        }
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        summary="Delete an existing rating",
        responses={
            204: OpenApiExample(
                'No Content',
                value=None,
                response_only=True,
                media_type='application/json',
            ),
            404: OpenApiExample(
                'Not Found',
                value={'detail': 'Not found.'},
                response_only=True,
                media_type='application/json',
            ),
        }
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)