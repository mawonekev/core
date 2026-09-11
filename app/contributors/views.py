from django.shortcuts import get_object_or_404
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import CreatorProfile
from .serializers import CreatorProfileSerializer


@extend_schema(
    tags=['Contributors'],
    summary='List all public contributors',
    responses={200: OpenApiResponse(response=CreatorProfileSerializer(many=True))}
)
@api_view(['GET'])
@permission_classes([AllowAny])
def contributor_list(request):
    contributors = CreatorProfile.objects.filter(is_public=True)
    serializer = CreatorProfileSerializer(contributors, many=True)
    return Response(serializer.data)


@extend_schema(
    tags=['Contributors'],
    summary='Retrieve public profile detail',
    responses={
        200: OpenApiResponse(response=CreatorProfileSerializer),
        404: OpenApiResponse(description='Not found'),
    }
)
@api_view(['GET'])
@permission_classes([AllowAny])
def contributor_detail(request, username):
    profile = get_object_or_404(CreatorProfile, username=username, is_public=True)
    serializer = CreatorProfileSerializer(profile)
    return Response(serializer.data)


@extend_schema(
    tags=['Contributors'],
    summary='Update own profile',
    description=(
        'Authenticated users can update **only their own** profile. '
        'Creating new profiles is **admin-only** (prevents impersonation).'
    ),
    request=CreatorProfileSerializer,
    responses={
        200: OpenApiResponse(response=CreatorProfileSerializer),
        401: OpenApiResponse(description='Authentication required.'),
        403: OpenApiResponse(description='Can only update your own profile.'),
        404: OpenApiResponse(description='Profile not found.'),
    }
)
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def profile_update(request):
    profile = get_object_or_404(CreatorProfile, user=request.user)
    serializer = CreatorProfileSerializer(profile, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
