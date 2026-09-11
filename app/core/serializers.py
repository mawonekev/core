from rest_framework import serializers

from .models import APIUsage, Statistics


class StatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statistics
        fields = [
            'total_attractions',
            'total_regions',
            'total_operators',
            'total_blog_articles',
            'total_users',
            'total_api_calls',
            'updated_at',
        ]


class APIUsageSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True, allow_null=True)

    class Meta:
        model = APIUsage
        fields = [
            'id',
            'endpoint',
            'method',
            'status_code',
            'ip_address',
            'user_agent',
            'response_time_ms',
            'user',
            'user_email',
            'timestamp',
        ]
        read_only_fields = [
            'id',
            'endpoint',
            'method',
            'status_code',
            'ip_address',
            'user_agent',
            'response_time_ms',
            'user',
            'timestamp',
        ]
