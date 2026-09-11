from django.contrib import admin
from django.db import models
from django.utils.html import format_html
from django_ckeditor_5.widgets import CKEditor5Widget
from unfold.admin import ModelAdmin, StackedInline, TabularInline

from .models import (
    Attraction,
    AttractionBoundary,
    AttractionImage,
    AttractionTip,
    Citation,
    EndemicSpecies,
    NearestTransport,
)


class AttractionImageInline(TabularInline):
    model = AttractionImage
    extra = 0
    min_num = 0
    fields = ['image', 'caption', 'order']


class AttractionTipInline(TabularInline):
    model = AttractionTip
    extra = 0
    min_num = 0
    fields = ['title', 'description', 'created_by']
    formfield_overrides = {
        models.TextField: {'widget': CKEditor5Widget(config_name='minimal')},
    }


class EndemicSpeciesInline(StackedInline):
    model = EndemicSpecies
    extra = 0
    min_num = 0
    fields = ['common_name', 'scientific_name', 'conservation_status', 'description', 'image']
    formfield_overrides = {
        models.TextField: {'widget': CKEditor5Widget(config_name='minimal')},
    }


class NearestTransportInline(TabularInline):
    model = NearestTransport
    extra = 0
    min_num = 0
    fields = [
        'transport_type', 'name', 'distance_km',
        'travel_time_minutes', 'is_recommended', 'description',
    ]


class AttractionBoundaryInline(StackedInline):
    model = AttractionBoundary
    extra = 0
    min_num = 0
    fields = [
        'boundary_type',
        'geojson',
        'center_latitude', 'center_longitude', 'radius_km',
        'bbox_north', 'bbox_south', 'bbox_east', 'bbox_west',
        'area_sq_km', 'elevation_min_m', 'elevation_max_m',
        'main_gate_name', 'main_gate_latitude', 'main_gate_longitude',
        'entry_points', 'zones',
    ]


@admin.register(Attraction)
class AttractionAdmin(ModelAdmin):
    list_display = [
        'name', 'region', 'category', 'difficulty_level',
        'approval_badge', 'deleted_badge', 'is_featured', 'is_active', 'created_at',
    ]
    list_filter = [
        'category', 'difficulty_level', 'region',
        'is_featured', 'is_active', 'is_approved', 'deleted_at',
    ]
    search_fields = ['name', 'description', 'short_description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at', 'deleted_at']
    actions = ['approve_action', 'reject_action', 'restore_action', 'soft_delete_action']
    inlines = [
        AttractionImageInline,
        AttractionTipInline,
        EndemicSpeciesInline,
        NearestTransportInline,
        AttractionBoundaryInline,
    ]

    formfield_overrides = {
        models.TextField: {'widget': CKEditor5Widget(config_name='default')},
    }

    fieldsets = (
        ('Basic Information', {
            'fields': (
                'name', 'slug', 'region', 'category',
                'short_description', 'description', 'featured_image', 'image_alt',
            )
        }),
        ('Location & GPS', {
            'description': 'Click on the map below to set coordinates, or drag the marker.',
            'fields': ('latitude', 'longitude', 'altitude', 'nearest_airport', 'distance_from_airport'),
            'classes': ['map-picker-fieldset'],
        }),
        ('Difficulty & Access', {
            'fields': ('difficulty_level', 'access_info', 'requires_guide', 'requires_permit', 'tags'),
        }),
        ('Timing & Seasons', {
            'fields': ('best_time_to_visit', 'seasonal_availability', 'estimated_duration'),
        }),
        ('Pricing', {
            'fields': ('price_from', 'price_to', 'currency', 'is_free', 'entrance_fee'),
        }),
        ('SEO', {
            'fields': (
                'meta_title', 'meta_description', 'meta_keywords',
                'og_title', 'og_description', 'og_image',
                'schema_type', 'schema_json', 'sitemap_priority', 'sitemap_changefreq',
                'no_index', 'canonical_url',
            ),
            'classes': ['collapse'],
        }),
        ('Affiliate', {
            'fields': ('gyg_location_id',),
        }),
        ('Status', {
            'fields': ('is_approved', 'is_active', 'is_featured', 'created_by', 'deleted_at'),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ['collapse'],
        }),
    )

    class Media:
        js = ['admin/js/map_picker.js']

    def approval_badge(self, obj):
        if obj.is_approved:
            return format_html(
                '<span style="background:#16a34a;color:#fff;padding:2px 8px;border-radius:3px">✓ Approved</span>'
            )
        return format_html(
            '<span style="background:#ca8a04;color:#fff;padding:2px 8px;border-radius:3px">⊘ Pending</span>'
        )
    approval_badge.short_description = 'Approval'

    def deleted_badge(self, obj):
        if obj.is_deleted:
            return format_html(
                '<span style="background:#dc2626;color:#fff;padding:2px 8px;border-radius:3px">🗑 Deleted</span>'
            )
        return format_html(
            '<span style="background:#16a34a;color:#fff;padding:2px 8px;border-radius:3px">✓ Active</span>'
        )
    deleted_badge.short_description = 'Status'

    def approve_action(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f'{updated} attraction(s) approved.')
    approve_action.short_description = '✓ Approve selected'

    def reject_action(self, request, queryset):
        updated = queryset.update(is_approved=False)
        self.message_user(request, f'{updated} attraction(s) rejected.')
    reject_action.short_description = '⊘ Reject selected'

    def restore_action(self, request, queryset):
        updated = queryset.update(deleted_at=None)
        self.message_user(request, f'{updated} attraction(s) restored.')
    restore_action.short_description = '↺ Restore deleted'

    def soft_delete_action(self, request, queryset):
        for obj in queryset:
            obj.delete()
        self.message_user(request, f'{queryset.count()} attraction(s) moved to trash.')
    soft_delete_action.short_description = '🗑 Move to trash'


@admin.register(EndemicSpecies)
class EndemicSpeciesAdmin(ModelAdmin):
    list_display = ['common_name', 'scientific_name', 'attraction', 'conservation_status']
    list_filter = ['conservation_status', 'attraction']
    search_fields = ['common_name', 'scientific_name']
    formfield_overrides = {
        models.TextField: {'widget': CKEditor5Widget(config_name='minimal')},
    }


@admin.register(Citation)
class CitationAdmin(ModelAdmin):
    list_display = ['title', 'author', 'citation_type', 'year', 'is_primary_source', 'trust_score']
    list_filter = ['citation_type', 'year', 'is_primary_source']
    search_fields = ['title', 'author', 'publisher', 'journal']
    filter_horizontal = ['attractions', 'regions', 'endemic_species', 'articles']
    fieldsets = (
        ('Source', {
            'fields': ('title', 'author', 'year', 'citation_type', 'publisher', 'journal'),
        }),
        ('Identifiers', {
            'fields': ('doi', 'isbn', 'url', 'accessed_date'),
        }),
        ('Linked Content', {
            'fields': ('attractions', 'regions', 'endemic_species', 'articles'),
        }),
        ('Quality', {
            'fields': ('is_primary_source', 'trust_score', 'formatted_citation'),
        }),
    )


@admin.register(NearestTransport)
class NearestTransportAdmin(ModelAdmin):
    list_display = ['name', 'transport_type', 'distance_km', 'attraction', 'is_recommended']
    list_filter = ['transport_type', 'is_recommended']
    search_fields = ['name', 'attraction__name']
    ordering = ['distance_km']


@admin.register(AttractionImage)
class AttractionImageAdmin(ModelAdmin):
    list_display = ['attraction', 'caption', 'order', 'uploaded_at']
    list_filter = ['attraction']


@admin.register(AttractionTip)
class AttractionTipAdmin(ModelAdmin):
    list_display = ['attraction', 'title', 'created_by', 'created_at']
    list_filter = ['attraction', 'created_at']
    formfield_overrides = {
        models.TextField: {'widget': CKEditor5Widget(config_name='minimal')},
    }
