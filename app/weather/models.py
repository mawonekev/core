from django.db import models

from app.attractions.models import Attraction


class WeatherCache(models.Model):
    attraction = models.OneToOneField(Attraction, on_delete=models.CASCADE, related_name='weather_cache')

    # Current weather
    temperature = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    apparent_temperature = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    precipitation = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    rain = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    weather_code = models.IntegerField(null=True)
    cloud_cover = models.IntegerField(null=True)
    wind_speed = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    humidity = models.IntegerField(null=True)

    # Seasonal pattern (JSON field for monthly averages)
    monthly_temperature = models.JSONField(default=dict, blank=True)
    monthly_precipitation = models.JSONField(default=dict, blank=True)

    # Metadata
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Weather cache'

    def __str__(self):
        return f"Weather for {self.attraction.name}"


class SeasonalWeatherPattern(models.Model):
    SEASON_CHOICES = [
        ('dry', 'Dry Season'),
        ('short_rain', 'Short Rain Season'),
        ('long_rain', 'Long Rain Season'),
    ]

    attraction = models.ForeignKey(Attraction, on_delete=models.CASCADE, related_name='seasonal_patterns')
    season_type = models.CharField(max_length=20, choices=SEASON_CHOICES)
    start_month = models.IntegerField()
    end_month = models.IntegerField()
    avg_temperature = models.DecimalField(max_digits=5, decimal_places=2)
    avg_rainfall = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField()

    class Meta:
        ordering = ['start_month']

    def __str__(self):
        return f"{self.attraction.name} - {self.get_season_type_display()}"
