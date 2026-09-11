from rest_framework import serializers

from .models import Announcement


class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = [
            'id', 'title', 'message', 'announcement_type', 'priority',
            'is_active', 'starts_at', 'ends_at', 'target_url', 'target_label',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class AnnouncementCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = [
            'title', 'message', 'announcement_type', 'priority',
            'is_active', 'starts_at', 'ends_at', 'target_url', 'target_label',
        ]
