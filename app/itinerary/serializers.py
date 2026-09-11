from rest_framework import serializers

from app.attractions.serializers import AttractionListSerializer

from .models import Itinerary, ItineraryActivity, ItineraryDay


class ItineraryActivitySerializer(serializers.ModelSerializer):
    attraction_name = serializers.CharField(source='attraction.name', read_only=True)
    attraction_slug = serializers.CharField(source='attraction.slug', read_only=True)

    class Meta:
        model = ItineraryActivity
        fields = ['id', 'attraction', 'attraction_name', 'attraction_slug', 'title', 'description',
                  'start_time', 'duration_hours', 'estimated_cost_usd', 'order', 'notes']


class ItineraryDaySerializer(serializers.ModelSerializer):
    activities = ItineraryActivitySerializer(many=True, read_only=True)

    class Meta:
        model = ItineraryDay
        fields = ['id', 'day_number', 'title', 'description', 'accommodation_notes', 'meals_notes', 'activities']


class ItineraryListSerializer(serializers.ModelSerializer):
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    attraction_count = serializers.SerializerMethodField()
    difficulty_display = serializers.CharField(source='get_difficulty_level_display', read_only=True)

    class Meta:
        model = Itinerary
        fields = ['id', 'title', 'slug', 'description', 'total_days', 'estimated_budget_usd',
                  'difficulty_level', 'difficulty_display', 'is_public', 'attraction_count',
                  'created_by_username', 'created_at']

    def get_attraction_count(self, obj):
        return obj.featured_attractions.count()


class ItineraryDetailSerializer(serializers.ModelSerializer):
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    difficulty_display = serializers.CharField(source='get_difficulty_level_display', read_only=True)
    days = ItineraryDaySerializer(many=True, read_only=True)
    featured_attractions = AttractionListSerializer(many=True, read_only=True)

    class Meta:
        model = Itinerary
        fields = ['id', 'title', 'slug', 'description', 'total_days', 'estimated_budget_usd',
                  'difficulty_level', 'difficulty_display', 'is_public', 'featured_attractions',
                  'days', 'created_by_username', 'created_at', 'updated_at']


class ItineraryCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Itinerary
        fields = ['title', 'slug', 'description', 'total_days', 'estimated_budget_usd',
                  'difficulty_level', 'is_public', 'featured_attractions']
