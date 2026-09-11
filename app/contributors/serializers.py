from rest_framework import serializers

from .models import CreatorProfile


class CreatorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreatorProfile
        fields = [
            'username', 'display_name', 'avatar', 'avatar_alt', 'bio',
            'job_title', 'organisation', 'expertise', 'website',
            'github_username', 'twitter_handle', 'instagram_handle',
            'linkedin_url', 'email_public', 'location_city', 'location_country',
            'attractions_created', 'attractions_edited', 'media_uploaded',
            'articles_written', 'species_added', 'is_public', 'is_verified_creator',
            'joined_at'
        ]
        read_only_fields = [
            'attractions_created', 'attractions_edited', 'media_uploaded',
            'articles_written', 'species_added', 'is_verified_creator', 'joined_at'
        ]
