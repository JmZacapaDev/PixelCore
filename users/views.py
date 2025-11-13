from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import UserRegistrationSerializer, UserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample

class UserRegistrationView(generics.CreateAPIView):
    """
    API endpoint for user registration.
    Allows new users to create an account.
    """
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)

    @extend_schema(
        summary="Register a new user",
        request=UserRegistrationSerializer,
        responses={
            201: OpenApiExample(
                'User Registration Success',
                value={'user_id': 'uuid', 'email': 'test@example.com', 'username': 'testuser'},
                response_only=True,
                media_type='application/json',
            ),
            400: OpenApiExample(
                'Bad Request',
                value={'email': ['This field must be unique.'], 'password': ["Password fields didn't match."]},
                response_only=True,
                media_type='application/json',
            ),
        },
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Customized API endpoint for obtaining JWT tokens.
    Returns access and refresh tokens upon successful authentication.
    """
    @extend_schema(
        summary="Obtain JWT tokens",
        request=OpenApiExample(
            'Login Request',
            value={'email': 'test@example.com', 'password': 'password123'},
            media_type='application/json',
        ),
        responses={
            200: OpenApiExample(
                'Token Obtain Success',
                value={'refresh': 'jwt_refresh_token', 'access': 'jwt_access_token'},
                response_only=True,
                media_type='application/json',
            ),
            401: OpenApiExample(
                'Unauthorized',
                value={'detail': 'No active account found with the given credentials'},
                response_only=True,
                media_type='application/json',
            ),
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)