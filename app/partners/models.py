from cloudinary.models import CloudinaryField
from django.db import models

from app.core.mixins import ContactMixin, ImageMixin, SEOMixin


class Partner(SEOMixin, ContactMixin, ImageMixin, models.Model):
    TIER_CHOICES = [
        ('platinum', 'Platinum'),
        ('gold', 'Gold'),
        ('silver', 'Silver'),
        ('community', 'Community'),
    ]

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    logo = CloudinaryField('image', blank=True, null=True, help_text='Partner logo')
    tier = models.CharField(max_length=20, choices=TIER_CHOICES, default='community')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['tier', 'name']
        indexes = [
            models.Index(fields=['tier']),
        ]

    def __str__(self):
        return f'{self.name} ({self.get_tier_display()})'
