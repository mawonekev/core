from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin

from .models import Media


@admin.register(Media)
class MediaAdmin(ModelAdmin):
    list_display = ['preview', 'title', 'media_type', 'approval_badge', 'license', 'uploaded_by', 'created_at']
    list_filter = ['media_type', 'is_approved', 'license']
    search_fields = ['title', 'alt_text', 'caption', 'credit']
    readonly_fields = ['created_at', 'updated_at', 'preview']
    actions = ['approve_action', 'reject_action']

    fieldsets = (
        ('File', {
            'fields': ('preview', 'file', 'media_type', 'title', 'alt_text', 'caption'),
        }),
        ('Attribution', {
            'fields': ('credit', 'license'),
        }),
        ('Meta', {
            'fields': ('uploaded_by', 'is_approved'),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    def preview(self, obj):
        if obj.file and obj.media_type == 'image':
            return format_html('<img src="{}" style="height:48px;width:72px;object-fit:cover;border-radius:4px" />', obj.file.url)
        return '—'
    preview.short_description = 'Preview'

    def approval_badge(self, obj):
        if obj.is_approved:
            return format_html('<span style="background:#16a34a;color:#fff;padding:2px 8px;border-radius:3px">Approved</span>')
        return format_html('<span style="background:#ca8a04;color:#fff;padding:2px 8px;border-radius:3px">Pending</span>')
    approval_badge.short_description = 'Approval'

    def approve_action(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, f'{queryset.count()} file(s) approved.')
    approve_action.short_description = 'Approve selected'

    def reject_action(self, request, queryset):
        queryset.update(is_approved=False)
        self.message_user(request, f'{queryset.count()} file(s) rejected.')
    reject_action.short_description = 'Reject selected'
