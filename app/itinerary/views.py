from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import Itinerary, ItineraryDay
from .serializers import (
    ItineraryActivitySerializer,
    ItineraryCreateUpdateSerializer,
    ItineraryDaySerializer,
    ItineraryDetailSerializer,
    ItineraryListSerializer,
)


@extend_schema(tags=['Itinerary'], summary='List itineraries', description='Get all public itineraries for Tanzania tour planning.')
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def itinerary_list_create(request):
    if request.method == 'GET':
        qs = Itinerary.objects.filter(is_public=True).prefetch_related('featured_attractions', 'days')
        difficulty = request.query_params.get('difficulty')
        days = request.query_params.get('days')
        if difficulty:
            qs = qs.filter(difficulty_level=difficulty)
        if days:
            qs = qs.filter(total_days=days)
        serializer = ItineraryListSerializer(qs, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ItineraryCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Itinerary'], summary='Itinerary detail')
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def itinerary_detail(request, slug):
    itinerary = get_object_or_404(Itinerary, slug=slug, is_public=True)
    if request.method == 'GET':
        serializer = ItineraryDetailSerializer(itinerary)
        return Response(serializer.data)
    elif request.method in ['PUT', 'PATCH']:
        serializer = ItineraryCreateUpdateSerializer(itinerary, data=request.data, partial=request.method == 'PATCH')
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        itinerary.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=['Itinerary'], summary='Manage itinerary days')
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def itinerary_days(request, slug):
    itinerary = get_object_or_404(Itinerary, slug=slug)
    if request.method == 'GET':
        serializer = ItineraryDaySerializer(itinerary.days.prefetch_related('activities'), many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ItineraryDaySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(itinerary=itinerary)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Itinerary'], summary='Add activity to a day')
@api_view(['POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def add_activity(request, day_id):
    day = get_object_or_404(ItineraryDay, pk=day_id)
    serializer = ItineraryActivitySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(day=day)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
