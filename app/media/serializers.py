from rest_framework import serializers

from .models import Media


class MediaSerializer(serializers.ModelSerializer):
    uploaded_by_username = serializers.CharField(source='uploaded_by.username', read_only=True)
    media_type_display = serializers.CharField(source='get_media_type_display', read_only=True)

    class Meta:
        model = Media
        fields = [
            'id', 'file', 'url', 'media_type', 'media_type_display',
            'title', 'alt_text', 'caption', 'credit', 'credit_url',
            'license', 'is_cover', 'is_featured', 'sort_order',
            'width', 'height', 'file_size_kb', 'taken_at',
            'location_name', 'latitude', 'longitude', 'is_approved',
            'uploaded_by_username', 'created_at', 'updated_at'
        ]
        read_only_fields = ['is_approved']
