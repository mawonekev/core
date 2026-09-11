from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin

from .models import Announcement


@admin.register(Announcement)
class AnnouncementAdmin(ModelAdmin):
    list_display = ['title', 'type_badge', 'priority_badge', 'is_active', 'starts_at', 'ends_at']
    list_filter = ['announcement_type', 'priority', 'is_active']
    search_fields = ['title', 'message']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Content', {
            'fields': ('title', 'message', 'announcement_type', 'priority'),
        }),
        ('Call to Action', {
            'fields': ('target_url', 'target_label'),
        }),
        ('Schedule', {
            'fields': ('is_active', 'starts_at', 'ends_at'),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    def type_badge(self, obj):
        colours = {
            'info': '#2563eb', 'warning': '#ca8a04',
            'success': '#16a34a', 'promo': '#7c3aed', 'maintenance': '#dc2626',
        }
        colour = colours.get(obj.announcement_type, '#6b7280')
        return format_html(
            '<span style="background:{};color:#fff;padding:2px 8px;border-radius:3px">{}</span>',
            colour, obj.get_announcement_type_display()
        )
    type_badge.short_description = 'Type'

    def priority_badge(self, obj):
        colours = {'low': '#9ca3af', 'normal': '#2563eb', 'high': '#ca8a04', 'urgent': '#dc2626'}
        colour = colours.get(obj.priority, '#6b7280')
        return format_html(
            '<span style="background:{};color:#fff;padding:2px 8px;border-radius:3px">{}</span>',
            colour, obj.get_priority_display()
        )
    priority_badge.short_description = 'Priority'
