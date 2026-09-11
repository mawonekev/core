from django.contrib.auth import get_user_model
from django.db import models

from app.attractions.models import Attraction
from app.core.mixins import ImageMixin, PublishMixin, SEOMixin
from app.core.models import BaseModel

User = get_user_model()


class Article(BaseModel, SEOMixin, ImageMixin, PublishMixin, models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    excerpt = models.CharField(max_length=400, help_text='Short teaser shown on listing cards')
    content = models.TextField(help_text='Full article body (supports Markdown)')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='articles')
    tags = models.ManyToManyField('core.Tag', blank=True, related_name='articles')
    related_attractions = models.ManyToManyField(
        Attraction, blank=True, related_name='blog_articles',
        help_text='Attractions mentioned or featured in this article'
    )

    # Legacy field - keeping for backward compatibility during transition
    is_published = models.BooleanField(default=False, help_text='Deprecated: Use status field instead')

    class Meta:
        ordering = ['-published_at', '-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['published_at']),
            models.Index(fields=['is_published']),  # Keep for backward compatibility
        ]

    def __str__(self):
        return self.title
