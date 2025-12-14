from drf_spectacular.utils import (OpenApiExample, OpenApiResponse,
                                   OpenApiTypes, extend_schema)
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import \
    TokenObtainPairView as BaseTokenObtainPairView
from rest_framework_simplejwt.views import \
    TokenRefreshView as BaseTokenRefreshView

from users.serializers import UserRegistrationSerializer


@extend_schema(
    summary="Register a new user",
    description="Creates a new user account with email and password. Returns the created user's data.",
    tags=["Authentication"],
    responses={
        status.HTTP_201_CREATED: UserRegistrationSerializer,
        status.HTTP_400_BAD_REQUEST: OpenApiResponse(
            response=OpenApiTypes.OBJECT,
            description="Validation errors (e.g., email exists, passwords mismatch).",
            examples=[
                OpenApiExample(
                    name='Missing/Blank fields',
                    value={
                        'email': ['This field is required', 'This field may not be blank'],
                        'password': ['This field is required', 'This field may not be blank'],
                        'password_confirmation': ['This field is required', 'This field may not be blank']
                    }
                ),
                OpenApiExample(
                    name='Email already exists',
                    value={'email': ['A user with that email already exists.']}
                ),
                OpenApiExample(
                    name='Password Mismatch',
                    value={'password_confirmation': ['Password and password confirmation do not match.']}
                ),
                OpenApiExample(
                    name='Weak Password',
                    value={'password': ['This password is too short. It must contain at least 8 characters.', '...']}
                )
            ]
        )
    }
)
class RegisterUserView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer

@extend_schema(
    summary="Login (Obtain Token Pair)",
    description="Takes a set of user credentials (email/password) and returns an access and refresh JSON web token pair.",
    tags=["Authentication"],
    responses={
        status.HTTP_200_OK: OpenApiResponse(
            description="Successful login returning JWT pair.",
            response=OpenApiTypes.OBJECT,
            examples=[
                OpenApiExample(
                    name='Success',
                    value={
                        'access': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...',
                        'refresh': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...'
                    }
                )
            ]
        ),
        status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
            response=OpenApiTypes.OBJECT,
            description="Authentication failed.",
            examples=[
                OpenApiExample(
                    name='Login Failed',
                    value={'detail': 'No active account found with the given credentials'}
                )
            ]
        )
    }
)
class TokenObtainPairView(BaseTokenObtainPairView):
    pass


@extend_schema(
    summary="Refresh Access Token",
    description="Takes a valid refresh token and returns a new access token. This is used when the 'access' token has expired but the user session is still valid.",
    tags=["Authentication"],
    responses={
        status.HTTP_200_OK: OpenApiResponse(
            description="New access token generated.",
            response=OpenApiTypes.OBJECT,
            examples=[
                OpenApiExample(
                    name='Success',
                    value={'access': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...'}
                )
            ]
        ),
        status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
            response=OpenApiTypes.OBJECT,
            description="Refresh token is invalid or expired.",
            examples=[
                OpenApiExample(
                    name='Token Expired',
                    summary='The refresh token has passed its lifetime.',
                    value={'detail': 'Token is invalid or expired', 'code': 'token_not_valid'}
                ),
                OpenApiExample(
                    name='Token Blacklisted',
                    summary='The token has been revoked or blacklisted.',
                    value={'detail': 'Token is blacklisted', 'code': 'token_not_valid'}
                )
            ]
        )
    }
)
class TokenRefreshView(BaseTokenRefreshView):
    pass