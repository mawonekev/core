from django.shortcuts import get_object_or_404
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import Media
from .serializers import MediaSerializer


@extend_schema(
    tags=['Media'],
    summary='List or upload media',
    responses={
        200: OpenApiResponse(response=MediaSerializer(many=True)),
        201: OpenApiResponse(response=MediaSerializer),
    }
)
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def media_list_create(request):
    if request.method == 'GET':
        media = Media.objects.filter(is_approved=True)
        serializer = MediaSerializer(media, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = MediaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(uploaded_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=['Media'],
    summary='Retrieve or delete a media item',
    responses={
        200: OpenApiResponse(response=MediaSerializer),
        204: OpenApiResponse(description='Deleted successfully.'),
    }
)
@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def media_detail(request, pk):
    media = get_object_or_404(Media, pk=pk)

    if request.method == 'GET':
        if not media.is_approved and request.user != media.uploaded_by and not request.user.is_staff:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = MediaSerializer(media)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        if request.user == media.uploaded_by or request.user.is_staff:
            media.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
