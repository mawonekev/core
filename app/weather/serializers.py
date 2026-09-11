from rest_framework import serializers

from .models import SeasonalWeatherPattern, WeatherCache
from .services import WeatherService


class WeatherCacheSerializer(serializers.ModelSerializer):
    attraction_name = serializers.CharField(source='attraction.name', read_only=True)
    weather_description = serializers.SerializerMethodField()

    class Meta:
        model = WeatherCache
        fields = [
            'attraction_name', 'temperature', 'apparent_temperature', 'precipitation',
            'rain', 'weather_code', 'weather_description', 'cloud_cover', 'wind_speed',
            'humidity', 'last_updated'
        ]

    def get_weather_description(self, obj):
        return WeatherService.get_weather_code_description(obj.weather_code) if obj.weather_code else 'Unknown'


class SeasonalWeatherPatternSerializer(serializers.ModelSerializer):
    season_display = serializers.CharField(source='get_season_type_display', read_only=True)

    class Meta:
        model = SeasonalWeatherPattern
        fields = [
            'id', 'season_type', 'season_display', 'start_month', 'end_month',
            'avg_temperature', 'avg_rainfall', 'description'
        ]


class CurrentWeatherSerializer(serializers.Serializer):
    temperature = serializers.FloatField()
    apparent_temperature = serializers.FloatField()
    humidity = serializers.IntegerField()
    precipitation = serializers.FloatField()
    rain = serializers.FloatField()
    weather_code = serializers.IntegerField()
    weather_description = serializers.CharField()
    cloud_cover = serializers.IntegerField()
    wind_speed = serializers.FloatField()
    timestamp = serializers.CharField()
