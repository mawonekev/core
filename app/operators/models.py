from cloudinary.models import CloudinaryField
from django.db import models

from app.attractions.models import Attraction
from app.core.mixins import ContactMixin, ImageMixin, PriceMixin, SEOMixin
from app.core.models import BaseModel


class TourOperator(BaseModel, SEOMixin, ContactMixin, ImageMixin, PriceMixin, models.Model):
    TIER_CHOICES = [
        ('budget', 'Budget'),
        ('mid', 'Mid-Range'),
        ('luxury', 'Luxury'),
    ]

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    short_description = models.CharField(max_length=300)
    logo = CloudinaryField('image', blank=True, null=True, help_text='Company logo')

    # Location (optional for operators)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, help_text='Office GPS latitude')
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, help_text='Office GPS longitude')
    address = models.CharField(max_length=500, blank=True, help_text='Office physical address')
    city = models.CharField(max_length=100, blank=True, help_text='Office city')
    region = models.ForeignKey(
        'regions.Region',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tour_operators',
        help_text='Primary operating region'
    )

    # Tags
    tags = models.ManyToManyField('core.Tag', blank=True, related_name='tour_operators')

    # Relationships
    attractions = models.ManyToManyField(
        Attraction,
        blank=True,
        related_name='operators',
        help_text='Attractions this operator covers'
    )
    tier = models.CharField(max_length=20, choices=TIER_CHOICES, default='mid')
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-is_verified', 'name']
        indexes = [
            models.Index(fields=['tier']),
            models.Index(fields=['is_verified']),
        ]

    def __str__(self):
        return self.name
