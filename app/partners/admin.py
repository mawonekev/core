from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin

from .models import Partner


@admin.register(Partner)
class PartnerAdmin(ModelAdmin):
    list_display = ['logo_preview', 'name', 'tier_badge', 'website', 'is_active', 'created_at']
    list_filter = ['tier', 'is_active']
    search_fields = ['name', 'description', 'email', 'website']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at', 'logo_preview']

    fieldsets = (
        ('Basic', {
            'fields': ('logo_preview', 'logo', 'name', 'slug', 'description', 'tier', 'is_active'),
        }),
        ('Contact', {
            'fields': ('website', 'email', 'phone', 'phone_secondary', 'whatsapp'),
        }),
        ('Social', {
            'fields': ('facebook', 'instagram', 'twitter'),
            'classes': ('collapse',),
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords', 'canonical_url', 'no_index'),
            'classes': ('collapse',),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="height:40px;width:40px;object-fit:contain;border-radius:4px" />', obj.logo.url)
        return '—'
    logo_preview.short_description = 'Logo'

    def tier_badge(self, obj):
        colors = {
            'platinum': '#7c3aed',
            'gold': '#ca8a04',
            'silver': '#6b7280',
            'community': '#1A4731',
        }
        color = colors.get(obj.tier, '#6b7280')
        return format_html(
            '<span style="background:{};color:#fff;padding:2px 8px;border-radius:3px;font-size:11px">{}</span>',
            color, obj.get_tier_display()
        )
    tier_badge.short_description = 'Tier'
