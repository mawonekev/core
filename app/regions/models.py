from cloudinary.models import CloudinaryField
from django.contrib.auth import get_user_model
from django.db import models

from app.core.mixins import SEOMixin
from app.core.models import BaseModel

User = get_user_model()


class Region(BaseModel, SEOMixin, models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField()
    image = CloudinaryField('image', blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    # Spatial data for maps
    boundary_geojson = models.JSONField(
        null=True,
        blank=True,
        help_text='GeoJSON boundary data for displaying region on map'
    )
    area_sq_km = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text='Area in square kilometers'
    )
    population = models.IntegerField(
        null=True,
        blank=True,
        help_text='Estimated population'
    )

    gyg_location_id = models.CharField(
        max_length=20, blank=True,
        help_text='GetYourGuide location ID for affiliate widget (e.g. 1202)'
    )

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_regions')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='updated_regions')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
