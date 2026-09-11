from django.contrib.auth import get_user_model
from django.db import models

from app.attractions.models import Attraction

User = get_user_model()


class Itinerary(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('moderate', 'Moderate'),
        ('challenging', 'Challenging'),
        ('difficult', 'Difficult'),
        ('extreme', 'Extreme'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    total_days = models.PositiveIntegerField()
    estimated_budget_usd = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text='Estimated total budget in USD')
    difficulty_level = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='moderate')
    is_public = models.BooleanField(default=True)
    featured_attractions = models.ManyToManyField(Attraction, blank=True, related_name='itineraries', help_text='Main attractions covered in this itinerary')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='itineraries')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Itineraries'
        indexes = [
            models.Index(fields=['difficulty_level']),
            models.Index(fields=['is_public']),
        ]

    def __str__(self):
        return self.title


class ItineraryDay(models.Model):
    itinerary = models.ForeignKey(Itinerary, on_delete=models.CASCADE, related_name='days')
    day_number = models.PositiveIntegerField()
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    accommodation_notes = models.TextField(blank=True, help_text='Where to stay, camp, or rest')
    meals_notes = models.TextField(blank=True, help_text='Meal recommendations for the day')

    class Meta:
        ordering = ['day_number']
        unique_together = ['itinerary', 'day_number']

    def __str__(self):
        return f"{self.itinerary.title} — Day {self.day_number}: {self.title}"


class ItineraryActivity(models.Model):
    day = models.ForeignKey(ItineraryDay, on_delete=models.CASCADE, related_name='activities')
    attraction = models.ForeignKey(Attraction, on_delete=models.SET_NULL, null=True, blank=True, related_name='itinerary_activities')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_time = models.TimeField(null=True, blank=True, help_text='Recommended start time')
    duration_hours = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    estimated_cost_usd = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    order = models.PositiveIntegerField(default=0)
    notes = models.TextField(blank=True, help_text='Tips, warnings, or special instructions')

    class Meta:
        ordering = ['order', 'start_time']

    def __str__(self):
        return f"Day {self.day.day_number} — {self.title}"
