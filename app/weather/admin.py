from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import SeasonalWeatherPattern, WeatherCache


@admin.register(WeatherCache)
class WeatherCacheAdmin(ModelAdmin):
    list_display = ['attraction', 'temperature', 'precipitation', 'humidity', 'wind_speed', 'last_updated']
    readonly_fields = ['last_updated']
    search_fields = ['attraction__name']

    fieldsets = (
        ('Attraction', {
            'fields': ('attraction',),
        }),
        ('Current Conditions', {
            'fields': ('temperature', 'apparent_temperature', 'weather_code', 'cloud_cover', 'humidity'),
        }),
        ('Precipitation & Wind', {
            'fields': ('precipitation', 'rain', 'wind_speed'),
        }),
        ('Monthly Averages', {
            'fields': ('monthly_temperature', 'monthly_precipitation'),
            'classes': ('collapse',),
        }),
        ('Meta', {
            'fields': ('last_updated',),
            'classes': ('collapse',),
        }),
    )


@admin.register(SeasonalWeatherPattern)
class SeasonalWeatherPatternAdmin(ModelAdmin):
    list_display = ['attraction', 'season_type', 'month_range', 'avg_temperature', 'avg_rainfall']
    list_filter = ['season_type']
    search_fields = ['attraction__name']

    fieldsets = (
        ('Attraction & Season', {
            'fields': ('attraction', 'season_type'),
        }),
        ('Period', {
            'fields': ('start_month', 'end_month'),
            'description': 'Use month numbers 1–12 (e.g. 1 = January, 12 = December).',
        }),
        ('Climate Data', {
            'fields': ('avg_temperature', 'avg_rainfall', 'description'),
        }),
    )

    def month_range(self, obj):
        months = ['', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                  'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        return f"{months[obj.start_month]} – {months[obj.end_month]}"
    month_range.short_description = 'Period'
