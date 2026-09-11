from django.db import models
from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Announcement
from .serializers import AnnouncementCreateSerializer, AnnouncementSerializer


def _active_qs():
    now = timezone.now()
    return Announcement.objects.filter(
        is_active=True,
        deleted_at__isnull=True,
    ).filter(
        models.Q(starts_at__isnull=True) | models.Q(starts_at__lte=now)
    ).filter(
        models.Q(ends_at__isnull=True) | models.Q(ends_at__gte=now)
    )


# Hidden from public Swagger — extend_schema(exclude=True) keeps it out of API docs
@extend_schema(exclude=True)
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def announcement_list_create(request):
    if request.method == 'GET':
        serializer = AnnouncementSerializer(_active_qs(), many=True)
        return Response(serializer.data)

    if not request.user.is_staff:
        return Response({'error': 'Admin only'}, status=status.HTTP_403_FORBIDDEN)

    serializer = AnnouncementCreateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(AnnouncementSerializer(serializer.instance).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(exclude=True)
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def announcement_detail(request, pk):
    try:
        announcement = Announcement.objects.get(pk=pk, deleted_at__isnull=True)
    except Announcement.DoesNotExist:
        return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        return Response(AnnouncementSerializer(announcement).data)

    if not request.user.is_staff:
        return Response({'error': 'Admin only'}, status=status.HTTP_403_FORBIDDEN)

    if request.method in ['PUT', 'PATCH']:
        serializer = AnnouncementCreateSerializer(
            announcement, data=request.data, partial=(request.method == 'PATCH')
        )
        if serializer.is_valid():
            serializer.save()
            return Response(AnnouncementSerializer(serializer.instance).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    announcement.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
