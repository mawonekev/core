import cloudinary
from rest_framework import serializers

from app.regions.serializers import RegionSerializer

from .models import (
    Attraction,
    AttractionBoundary,
    AttractionImage,
    AttractionTip,
    Citation,
    EndemicSpecies,
    NearestTransport,
)


class CloudinaryImageMixin:
    def get_featured_image(self, obj):
        if obj.featured_image:
            return cloudinary.CloudinaryImage(str(obj.featured_image)).build_url(secure=True)
        return None

class AttractionImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        if obj.image:
            return cloudinary.CloudinaryImage(str(obj.image)).build_url(secure=True)
        return None

    class Meta:
        model = AttractionImage
        fields = ['id', 'image', 'caption', 'order']

class AttractionTipSerializer(serializers.ModelSerializer):
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = AttractionTip
        fields = ['id', 'title', 'description', 'created_by_username', 'created_at']


class EndemicSpeciesSerializer(serializers.ModelSerializer):
    conservation_status_display = serializers.CharField(source='get_conservation_status_display', read_only=True)

    class Meta:
        model = EndemicSpecies
        fields = [
            'id', 'common_name', 'scientific_name', 'description',
            'image', 'conservation_status', 'conservation_status_display', 'created_at',
        ]


class AttractionBoundarySerializer(serializers.ModelSerializer):
    class Meta:
        model = AttractionBoundary
        fields = [
            'id', 'attraction', 'boundary_type', 'geojson',
            'center_latitude', 'center_longitude', 'radius_km',
            'bbox_north', 'bbox_south', 'bbox_east', 'bbox_west',
            'area_sq_km', 'perimeter_km', 'elevation_min_m', 'elevation_max_m',
            'main_gate_latitude', 'main_gate_longitude', 'main_gate_name',
            'entry_points', 'zones', 'created_at', 'updated_at'
        ]


class CitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Citation
        fields = [
            'id', 'title', 'author', 'year', 'citation_type',
            'publisher', 'journal', 'doi', 'url', 'isbn', 'accessed_date',
            'formatted_citation', 'is_primary_source', 'trust_score', 'created_at'
        ]


class NearestTransportSerializer(serializers.ModelSerializer):
    transport_type_display = serializers.SerializerMethodField()

    class Meta:
        model = NearestTransport
        fields = [
            'id', 'attraction', 'transport_type', 'transport_type_display', 'name',
            'distance_km', 'travel_time_minutes', 'latitude', 'longitude',
            'description', 'is_recommended', 'created_at',
        ]
        read_only_fields = ['id', 'created_at']

    def get_transport_type_display(self, obj):
        return obj.get_transport_type_display()


class AttractionListSerializer(CloudinaryImageMixin,serializers.ModelSerializer):
    featured_image = serializers.SerializerMethodField()
    region_name = serializers.CharField(source='region.name', read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    difficulty_display = serializers.CharField(source='get_difficulty_level_display', read_only=True)
    created_by_username = serializers.CharField(source='created_by.username', read_only=True, allow_null=True)

    class Meta:
        model = Attraction
        fields = [
            'id', 'name', 'slug', 'region_name', 'category', 'category_display',
            'short_description', 'difficulty_level', 'difficulty_display',
            'featured_image', 'is_featured', 'best_time_to_visit', 'created_by_username'
        ]


class AttractionDetailSerializer(CloudinaryImageMixin,serializers.ModelSerializer):
    featured_image = serializers.SerializerMethodField()
    region = RegionSerializer(read_only=True)
    images = AttractionImageSerializer(many=True, read_only=True)
    tips = AttractionTipSerializer(many=True, read_only=True)
    endemic_species = EndemicSpeciesSerializer(many=True, read_only=True)
    boundary = AttractionBoundarySerializer(read_only=True)
    transport_facilities = serializers.SerializerMethodField()
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    difficulty_display = serializers.CharField(source='get_difficulty_level_display', read_only=True)

    # Creator/Editor info
    created_by_username = serializers.CharField(source='created_by.username', read_only=True, allow_null=True)
    created_by_email = serializers.EmailField(source='created_by.email', read_only=True, allow_null=True)
    updated_by_username = serializers.CharField(source='updated_by.username', read_only=True, allow_null=True)

    # Tour operators offering this attraction
    tour_operators = serializers.SerializerMethodField()

    # Itineraries including this attraction
    itineraries = serializers.SerializerMethodField()

    class Meta:
        model = Attraction
        fields = [
            'id', 'name', 'slug', 'region', 'category', 'category_display',
            'description', 'short_description', 'latitude', 'longitude', 'altitude',
            'difficulty_level', 'difficulty_display', 'access_info', 'nearest_airport',
            'distance_from_airport', 'best_time_to_visit', 'seasonal_availability',
            'estimated_duration', 'entrance_fee', 'requires_guide', 'requires_permit',
            'featured_image', 'images', 'tips', 'endemic_species', 'boundary',
            'transport_facilities', 'is_featured',
            'created_by_username', 'created_by_email', 'updated_by_username',
            'tour_operators', 'itineraries',
            'created_at', 'updated_at'
        ]

    def get_transport_facilities(self, obj):
        return NearestTransportSerializer(obj.transport_facilities.all(), many=True).data

    def get_tour_operators(self, obj):
        """Return list of tour operators that offer this attraction"""
        from app.operators.serializers import TourOperatorListSerializer
        operators = obj.operators.filter(is_active=True, is_approved=True)
        return TourOperatorListSerializer(operators, many=True).data

    def get_itineraries(self, obj):
        """Return list of itineraries that include this attraction"""
        from app.itinerary.serializers import ItineraryListSerializer
        itineraries = obj.itineraries.filter(is_public=True)
        return ItineraryListSerializer(itineraries, many=True).data


class AttractionCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attraction
        fields = [
            'name', 'slug', 'region', 'category', 'description', 'short_description',
            'latitude', 'longitude', 'altitude', 'difficulty_level', 'access_info',
            'nearest_airport', 'distance_from_airport', 'best_time_to_visit',
            'seasonal_availability', 'estimated_duration', 'entrance_fee',
            'requires_guide', 'requires_permit', 'featured_image'
        ]
