from rest_framework import serializers

from .models import Article


class ArticleListSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True, allow_null=True)
    author_email = serializers.EmailField(source='author.email', read_only=True, allow_null=True)
    author_full_name = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = [
            'id', 'title', 'slug', 'excerpt', 'featured_image',
            'author_username', 'author_email', 'author_full_name', 'tags', 'published_at',
        ]

    def get_author_full_name(self, obj):
        if obj.author:
            full_name = f"{obj.author.first_name} {obj.author.last_name}".strip()
            return full_name or obj.author.username
        return None


class ArticleDetailSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True, allow_null=True)
    author_email = serializers.EmailField(source='author.email', read_only=True, allow_null=True)
    author_full_name = serializers.SerializerMethodField()
    related_attraction_slugs = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = [
            'id', 'title', 'slug', 'excerpt', 'content', 'featured_image',
            'author_username', 'author_email', 'author_full_name', 'tags', 'related_attraction_slugs',
            'is_published', 'published_at', 'created_at', 'updated_at',
        ]

    def get_author_full_name(self, obj):
        if obj.author:
            full_name = f"{obj.author.first_name} {obj.author.last_name}".strip()
            return full_name or obj.author.username
        return None

    def get_related_attraction_slugs(self, obj):
        return list(obj.related_attractions.values_list('slug', flat=True))


class ArticleCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = [
            'title', 'slug', 'excerpt', 'content', 'featured_image',
            'tags', 'related_attractions', 'is_published', 'published_at',
        ]
