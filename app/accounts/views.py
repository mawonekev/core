from django.contrib.auth import get_user_model
from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .serializers import CustomTokenObtainPairSerializer, RegisterSerializer, UserSerializer

User = get_user_model()


@extend_schema(
    tags=['Auth'],
    summary='Register a new user',
    description=(
        'Create a new user account.\n\n'
        '**Required fields:** `username`, `email`, `password`, `password_confirm`\n\n'
        '**Optional fields:** `phone`, `bio`\n\n'
        '**Password rules:** minimum 8 characters; `password` and `password_confirm` must match.\n\n'
        '**curl example:**\n'
        '```bash\n'
        'curl -X POST https://xenohuru.cleven.is-a.dev/api/v1/auth/register/ \\\n'
        '  -H "Content-Type: application/json" \\\n'
        '  -d \'{"username":"john","email":"john@example.com","password":"Secure123!","password_confirm":"Secure123!"}\'\n'
        '```'
    ),
    request=RegisterSerializer,
    responses={
        201: OpenApiResponse(
            response=UserSerializer,
            description='User created successfully. Returns the new user profile (passwords excluded).',
            examples=[
                OpenApiExample(
                    'Successful registration',
                    value={
                        'id': 5,
                        'username': 'john',
                        'email': 'john@example.com',
                        'phone': '',
                        'bio': '',
                        'is_tour_operator': False,
                        'date_joined': '2026-02-26T08:00:00Z',
                    },
                )
            ],
        ),
        400: OpenApiResponse(
            description='Validation error. Returned when required fields are missing, passwords do not match, or email/username is already taken.',
            examples=[
                OpenApiExample(
                    'Password mismatch',
                    value={'non_field_errors': ['Passwords do not match']},
                ),
                OpenApiExample(
                    'Missing fields',
                    value={
                        'username': ['This field is required.'],
                        'email': ['This field is required.'],
                        'password': ['This field is required.'],
                        'password_confirm': ['This field is required.'],
                    },
                ),
            ],
        ),
    },
    examples=[
        OpenApiExample(
            'Minimal registration',
            request_only=True,
            value={
                'username': 'john',
                'email': 'john@example.com',
                'password': 'Secure123!',
                'password_confirm': 'Secure123!',
            },
        ),
        OpenApiExample(
            'Full registration',
            request_only=True,
            value={
                'username': 'john',
                'email': 'john@example.com',
                'password': 'Secure123!',
                'password_confirm': 'Secure123!',
                'phone': '+255712345678',
                'bio': 'Safari enthusiast based in Arusha.',
            },
        ),
    ],
)
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=['Auth'],
    summary='Login — obtain JWT tokens',
    description=(
        'Authenticate with username and password. Returns a JWT `access` token (valid 60 min) '
        'and a `refresh` token (valid 24 h).\n\n'
        '**Note:** The login field is `username`, not `email`.\n\n'
        'Use the `access` token in subsequent requests as:\n'
        '```\nAuthorization: Bearer <access_token>\n```\n\n'
        '**curl example:**\n'
        '```bash\n'
        'curl -X POST https://xenohuru.cleven.is-a.dev/api/v1/auth/login/ \\\n'
        '  -H "Content-Type: application/json" \\\n'
        '  -d \'{"username":"john","password":"Secure123!"}\'\n'
        '```'
    ),
    request={
        'application/json': {
            'type': 'object',
            'required': ['username', 'password'],
            'properties': {
                'username': {'type': 'string', 'example': 'john'},
                'password': {'type': 'string', 'example': 'Secure123!'},
            },
        }
    },
    responses={
        200: OpenApiResponse(
            description='Login successful. Returns access and refresh JWT tokens.',
            examples=[
                OpenApiExample(
                    'Token response',
                    value={
                        'access': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...',
                        'refresh': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...',
                    },
                )
            ],
        ),
        401: OpenApiResponse(
            description='Invalid credentials.',
            examples=[
                OpenApiExample(
                    'Bad credentials',
                    value={'detail': 'No active account found with the given credentials'},
                )
            ],
        ),
    },
    examples=[
        OpenApiExample(
            'Login request',
            request_only=True,
            value={'username': 'john', 'password': 'Secure123!'},
        )
    ],
)
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    serializer = CustomTokenObtainPairSerializer(data=request.data, context={'request': request})
    serializer.is_valid(raise_exception=True)
    return Response(serializer.validated_data, status=status.HTTP_200_OK)


@extend_schema(
    tags=['Auth'],
    summary='Get or update own profile',
    description=(
        'Retrieve (GET), fully replace (PUT), or partially update (PATCH) the authenticated user\'s profile.\n\n'
        '**Authentication required:** `Authorization: Bearer <access_token>`\n\n'
        '**curl example (GET):**\n'
        '```bash\n'
        'curl https://xenohuru.cleven.is-a.dev/api/v1/auth/profile/ \\\n'
        '  -H "Authorization: Bearer <access_token>"\n'
        '```\n\n'
        '**curl example (PATCH):**\n'
        '```bash\n'
        'curl -X PATCH https://xenohuru.cleven.is-a.dev/api/v1/auth/profile/ \\\n'
        '  -H "Authorization: Bearer <access_token>" \\\n'
        '  -H "Content-Type: application/json" \\\n'
        '  -d \'{"bio":"Updated bio"}\'\n'
        '```'
    ),
    request=UserSerializer,
    responses={
        200: OpenApiResponse(
            response=UserSerializer,
            description='User profile.',
            examples=[
                OpenApiExample(
                    'Profile response',
                    value={
                        'id': 5,
                        'username': 'john',
                        'email': 'john@example.com',
                        'phone': '+255712345678',
                        'bio': 'Safari enthusiast.',
                        'is_tour_operator': False,
                        'date_joined': '2026-02-26T08:00:00Z',
                    },
                )
            ],
        ),
        401: OpenApiResponse(description='Authentication credentials were not provided or are invalid.'),
    },
    examples=[
        OpenApiExample(
            'Partial update (PATCH)',
            request_only=True,
            value={'bio': 'Updated bio text', 'phone': '+255700000000'},
        )
    ],
)
@api_view(['GET', 'PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    if not request.user or not request.user.is_authenticated:
        return Response(
            {'detail': 'Authentication credentials were not provided.'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    user = request.user
    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)
    serializer = UserSerializer(user, data=request.data, partial=request.method == 'PATCH')
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=['Auth'],
    summary='Verify email address',
    description=(
        'Verify user email using the token sent to their email.\n\n'
        'After successful registration, users receive an email with a verification link.\n'
        'This endpoint activates the account and allows full API access.\n\n'
        '**curl example:**\n'
        '```bash\n'
        'curl -X POST https://xenohuru.cleven.is-a.dev/api/v1/auth/verify-email/ \\\n'
        '  -H "Content-Type: application/json" \\\n'
        '  -d \'{"token":"550e8400-e29b-41d4-a716-446655440000"}\'\n'
        '```'
    ),
    request={
        'application/json': {
            'type': 'object',
            'required': ['token'],
            'properties': {
                'token': {'type': 'string', 'format': 'uuid', 'example': '550e8400-e29b-41d4-a716-446655440000'},
            },
        }
    },
    responses={
        200: OpenApiResponse(
            description='Email verified successfully.',
            examples=[
                OpenApiExample(
                    'Success',
                    value={'message': 'Email verified successfully', 'email_verified': True},
                )
            ],
        ),
        400: OpenApiResponse(
            description='Invalid or expired token.',
            examples=[
                OpenApiExample(
                    'Invalid token',
                    value={'error': 'Invalid or expired verification token'},
                ),
            ],
        ),
    },
)
@api_view(['POST'])
@permission_classes([AllowAny])
def verify_email(request):
    import logging

    from .emails import send_welcome_email
    logger = logging.getLogger('app.accounts')

    token = request.data.get('token')
    if not token:
        return Response({'error': 'Verification token is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(email_verification_token=token)

        # Check if already verified
        if user.is_email_verified:
            return Response({'message': 'Email already verified', 'email_verified': True})

        # Check if token is expired
        if user.is_verification_token_expired():
            return Response(
                {'error': 'Verification token has expired. Please request a new one.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Mark email as verified
        user.is_email_verified = True
        user.save(update_fields=['is_email_verified'])

        # Send welcome email
        send_welcome_email(user)

        logger.info(f"Email verified for user: {user.username} ({user.email})")

        return Response({
            'message': 'Email verified successfully',
            'email_verified': True
        })

    except User.DoesNotExist:
        return Response(
            {'error': 'Invalid or expired verification token'},
            status=status.HTTP_400_BAD_REQUEST
        )


@extend_schema(
    tags=['Auth'],
    summary='Resend verification email',
    description=(
        'Request a new verification email if the previous one expired or was not received.\n\n'
        '**curl example:**\n'
        '```bash\n'
        'curl -X POST https://xenohuru.cleven.is-a.dev/api/v1/auth/resend-verification/ \\\n'
        '  -H "Content-Type: application/json" \\\n'
        '  -d \'{"email":"john@example.com"}\'\n'
        '```'
    ),
    request={
        'application/json': {
            'type': 'object',
            'required': ['email'],
            'properties': {
                'email': {'type': 'string', 'format': 'email', 'example': 'john@example.com'},
            },
        }
    },
    responses={
        200: OpenApiResponse(
            description='Verification email sent.',
            examples=[
                OpenApiExample(
                    'Success',
                    value={'message': 'Verification email sent successfully'},
                )
            ],
        ),
        400: OpenApiResponse(
            description='Email already verified or not found.',
        ),
    },
)
@api_view(['POST'])
@permission_classes([AllowAny])
def resend_verification(request):
    import logging

    from .emails import send_verification_email
    logger = logging.getLogger('app.accounts')

    email = request.data.get('email')
    if not email:
        return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(email=email)

        # Check if already verified
        if user.is_email_verified:
            return Response(
                {'message': 'Email is already verified'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Regenerate token and send email
        user.regenerate_verification_token()
        send_verification_email(user)

        logger.info(f"Verification email resent to: {email}")

        return Response({'message': 'Verification email sent successfully'})

    except User.DoesNotExist:
        # Don't reveal if email exists or not
        return Response({'message': 'If the email exists, a verification link has been sent'})
