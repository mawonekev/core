from django.contrib import admin
from django.db import models
from django.utils.html import format_html
from django_ckeditor_5.widgets import CKEditor5Widget
from unfold.admin import ModelAdmin

from .models import Region


@admin.register(Region)
class RegionAdmin(ModelAdmin):
    list_display = [
        'name', 'slug', 'approval_badge', 'deleted_badge',
        'gyg_location_id', 'latitude', 'longitude', 'created_at',
    ]
    list_filter = ['is_approved', 'deleted_at', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at', 'deleted_at', 'boundary_map_widget']
    actions = ['approve_action', 'reject_action', 'restore_action', 'soft_delete_action']

    formfield_overrides = {
        models.TextField: {'widget': CKEditor5Widget(config_name='default')},
    }

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description', 'image'),
        }),
        ('Location & GPS', {
            'description': 'Click the map below to set coordinates, or drag the marker.',
            'fields': ('latitude', 'longitude', 'area_sq_km', 'population'),
        }),
        ('Map Boundary', {
            'fields': ('boundary_geojson', 'boundary_map_widget'),
            'description': (
                'Draw the region boundary on the map below, or paste raw GeoJSON into the field above '
                'then click "Reload from textarea". Get boundary data free from '
                '<a href="https://geojson.io" target="_blank">geojson.io</a> or '
                '<a href="https://overpass-turbo.eu" target="_blank">Overpass Turbo</a>.'
            ),
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
            'fields': ('is_approved', 'deleted_at'),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ['collapse'],
        }),
    )

    def boundary_map_widget(self, obj):
        return format_html(
            '<div style="margin-bottom:8px">'
            '<button type="button" id="boundary-import-btn" '
            'style="background:#1A4731;color:#fff;border:none;padding:6px 14px;border-radius:6px;cursor:pointer;font-size:13px">'
            'Reload from textarea</button>'
            '&nbsp;<span id="boundary-hint" style="font-size:12px;color:#666"></span></div>'
            '<div id="boundary-map-widget" '
            'style="height:420px;width:100%;border-radius:8px;overflow:hidden;border:1px solid #e5e7eb"></div>'
        )
    boundary_map_widget.short_description = 'Draw / Preview Boundary'

    class Media:
        js = ['admin/js/map_picker.js', 'admin/js/boundary_picker.js']

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
        self.message_user(request, f'{updated} region(s) approved.')
    approve_action.short_description = '✓ Approve selected'

    def reject_action(self, request, queryset):
        updated = queryset.update(is_approved=False)
        self.message_user(request, f'{updated} region(s) rejected.')
    reject_action.short_description = '⊘ Reject selected'

    def restore_action(self, request, queryset):
        updated = queryset.update(deleted_at=None)
        self.message_user(request, f'{updated} region(s) restored.')
    restore_action.short_description = '↺ Restore deleted'

    def soft_delete_action(self, request, queryset):
        for obj in queryset:
            obj.delete()
        self.message_user(request, f'{queryset.count()} region(s) moved to trash.')
    soft_delete_action.short_description = '🗑 Move to trash'
