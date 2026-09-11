from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin

from .models import TourOperator


@admin.register(TourOperator)
class TourOperatorAdmin(ModelAdmin):
    list_display = ['name', 'tier', 'approval_badge', 'status_badge', 'is_verified', 'is_active', 'created_at']
    list_filter = ['tier', 'is_verified', 'is_active', 'is_approved', 'deleted_at']
    search_fields = ['name', 'description', 'email']
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ['attractions']
    readonly_fields = ['created_at', 'updated_at', 'deleted_at']
    actions = ['approve_action', 'reject_action', 'restore_action', 'soft_delete_action']

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'short_description', 'description', 'logo'),
        }),
        ('Contact', {
            'fields': ('website', 'phone', 'email'),
        }),
        ('Classification', {
            'fields': ('tier', 'is_verified', 'is_active'),
        }),
        ('Attractions Covered', {
            'fields': ('attractions',),
        }),
        ('Status', {
            'fields': ('is_approved', 'deleted_at'),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    def approval_badge(self, obj):
        if obj.is_approved:
            return format_html('<span style="background:#16a34a;color:#fff;padding:2px 8px;border-radius:3px">Approved</span>')
        return format_html('<span style="background:#ca8a04;color:#fff;padding:2px 8px;border-radius:3px">Pending</span>')
    approval_badge.short_description = 'Approval'

    def status_badge(self, obj):
        if obj.is_deleted:
            return format_html('<span style="background:#dc2626;color:#fff;padding:2px 8px;border-radius:3px">Deleted</span>')
        return format_html('<span style="background:#16a34a;color:#fff;padding:2px 8px;border-radius:3px">Active</span>')
    status_badge.short_description = 'Status'

    def approve_action(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, f'{queryset.count()} operator(s) approved.')
    approve_action.short_description = 'Approve selected'

    def reject_action(self, request, queryset):
        queryset.update(is_approved=False)
        self.message_user(request, f'{queryset.count()} operator(s) rejected.')
    reject_action.short_description = 'Reject selected'

    def restore_action(self, request, queryset):
        queryset.update(deleted_at=None)
        self.message_user(request, f'{queryset.count()} operator(s) restored.')
    restore_action.short_description = 'Restore deleted'

    def soft_delete_action(self, request, queryset):
        for obj in queryset:
            obj.delete()
        self.message_user(request, f'{queryset.count()} operator(s) moved to trash.')
    soft_delete_action.short_description = 'Move to trash'
