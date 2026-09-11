from rest_framework import serializers

from .models import Review, UserFeedback


class UserFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFeedback
        fields = [
            'id', 'user', 'name', 'email', 'feedback_type',
            'subject', 'message', 'rating', 'content_type',
            'object_id', 'attachment', 'status', 'response',
            'created_at'
        ]
        read_only_fields = ['status', 'response', 'user']

class ReviewSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True, allow_null=True)

    class Meta:
        model = Review
        fields = [
            'id', 'user', 'username', 'reviewer_name', 'reviewer_email',
            'reviewer_country', 'attraction', 'title', 'body', 'rating',
            'rating_scenery', 'rating_accessibility', 'rating_value_for_money',
            'rating_safety', 'rating_facilities', 'visited_at', 'visit_type',
            'visit_season', 'photos', 'is_approved', 'helpful_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['user', 'username', 'is_approved', 'helpful_count', 'attraction']

    def validate(self, data):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            if not data.get('reviewer_name'):
                raise serializers.ValidationError({'reviewer_name': 'Name is required.'})
        if data.get('rating') and (data['rating'] < 1 or data['rating'] > 5):
            raise serializers.ValidationError({'rating': 'Rating must be between 1 and 5.'})
        return data
