from django.contrib import admin
from django.db import models
from django_ckeditor_5.widgets import CKEditor5Widget
from unfold.admin import ModelAdmin, StackedInline, TabularInline

from .models import Itinerary, ItineraryActivity, ItineraryDay


class ItineraryActivityInline(TabularInline):
    model = ItineraryActivity
    extra = 0
    min_num = 0
    fields = [
        'order', 'title', 'attraction', 'start_time',
        'duration_hours', 'estimated_cost_usd', 'notes',
    ]


class ItineraryDayInline(StackedInline):
    model = ItineraryDay
    extra = 0
    min_num = 0
    fields = ['day_number', 'title', 'description', 'accommodation_notes', 'meals_notes']
    formfield_overrides = {
        models.TextField: {'widget': CKEditor5Widget(config_name='minimal')},
    }


@admin.register(Itinerary)
class ItineraryAdmin(ModelAdmin):
    list_display = [
        'title', 'total_days', 'difficulty_level',
        'estimated_budget_usd', 'is_public', 'created_by', 'created_at',
    ]
    list_filter = ['difficulty_level', 'is_public', 'created_at']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['featured_attractions']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [ItineraryDayInline]
    formfield_overrides = {
        models.TextField: {'widget': CKEditor5Widget(config_name='default')},
    }
    fieldsets = (
        ('Overview', {
            'fields': (
                'title', 'slug', 'description',
                'total_days', 'difficulty_level', 'estimated_budget_usd', 'is_public',
            )
        }),
        ('Attractions', {
            'fields': ('featured_attractions',),
        }),
        ('Meta', {
            'fields': ('created_by', 'created_at', 'updated_at'),
        }),
    )


@admin.register(ItineraryDay)
class ItineraryDayAdmin(ModelAdmin):
    list_display = ['itinerary', 'day_number', 'title']
    list_filter = ['itinerary']
    search_fields = ['title', 'itinerary__title']
    inlines = [ItineraryActivityInline]
    formfield_overrides = {
        models.TextField: {'widget': CKEditor5Widget(config_name='minimal')},
    }


@admin.register(ItineraryActivity)
class ItineraryActivityAdmin(ModelAdmin):
    list_display = ['title', 'day', 'attraction', 'start_time', 'duration_hours', 'estimated_cost_usd', 'order']
    list_filter = ['day__itinerary', 'attraction']
    search_fields = ['title', 'notes', 'attraction__name']
    ordering = ['day__itinerary', 'day__day_number', 'order']
