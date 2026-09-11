from rest_framework import serializers

from .models import Region


class RegionSerializer(serializers.ModelSerializer):
    attraction_count = serializers.SerializerMethodField()
    created_by_username = serializers.CharField(source='created_by.username', read_only=True, allow_null=True)
    created_by_email = serializers.EmailField(source='created_by.email', read_only=True, allow_null=True)
    updated_by_username = serializers.CharField(source='updated_by.username', read_only=True, allow_null=True)

    class Meta:
        model = Region
        fields = [
            'id', 'name', 'slug', 'description', 'image', 'latitude', 'longitude',
            'boundary_geojson', 'area_sq_km', 'population',
            'attraction_count', 'created_by_username', 'created_by_email',
            'updated_by_username', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by_username', 'created_by_email', 'updated_by_username']

    def get_attraction_count(self, obj):
        return obj.attractions.count()
