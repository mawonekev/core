from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin

from .models import CreatorProfile


@admin.register(CreatorProfile)
class CreatorProfileAdmin(ModelAdmin):
    list_display = ['display_name', 'username', 'verified_badge', 'public_badge', 'expertise', 'joined_at']
    list_filter = ['is_verified_creator', 'is_public', 'expertise']
    search_fields = ['username', 'display_name', 'user__email', 'bio']
    readonly_fields = ['joined_at', 'updated_at']

    fieldsets = (
        ('Profile', {
            'fields': ('user', 'username', 'display_name', 'bio', 'avatar'),
        }),
        ('Expertise', {
            'fields': ('expertise', 'social_links'),
        }),
        ('Status', {
            'fields': ('is_verified_creator', 'is_public'),
        }),
        ('Timestamps', {
            'fields': ('joined_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    def verified_badge(self, obj):
        if obj.is_verified_creator:
            return format_html('<span style="background:#2563eb;color:#fff;padding:2px 8px;border-radius:3px">Verified</span>')
        return format_html('<span style="background:#d1d5db;color:#374151;padding:2px 8px;border-radius:3px">Unverified</span>')
    verified_badge.short_description = 'Creator'

    def public_badge(self, obj):
        if obj.is_public:
            return format_html('<span style="background:#16a34a;color:#fff;padding:2px 8px;border-radius:3px">Public</span>')
        return format_html('<span style="background:#6b7280;color:#fff;padding:2px 8px;border-radius:3px">Private</span>')
    public_badge.short_description = 'Visibility'
