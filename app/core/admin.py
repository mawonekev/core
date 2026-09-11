from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin

from .models import APIUsage, Statistics, Tag, UserActivityLog


@admin.register(Tag)
class TagAdmin(ModelAdmin):
    list_display = ['name', 'slug', 'description', 'created_at']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Statistics)
class StatisticsAdmin(ModelAdmin):
    readonly_fields = (
        'total_attractions', 'total_regions', 'total_operators',
        'total_blog_articles', 'total_users', 'total_api_calls', 'updated_at',
    )
    list_display = ('display_stats', 'updated_at')

    def display_stats(self, obj):
        return (
            f"Attractions: {obj.total_attractions} | Regions: {obj.total_regions} | "
            f"Operators: {obj.total_operators} | Articles: {obj.total_blog_articles} | "
            f"API Calls: {obj.total_api_calls}"
        )
    display_stats.short_description = 'System Statistics'

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(APIUsage)
class APIUsageAdmin(ModelAdmin):
    list_display = (
        'timestamp', 'method_badge', 'endpoint',
        'status_badge', 'response_time_ms', 'user', 'ip_address',
    )
    list_filter = ('method', 'status_code', 'timestamp', 'user')
    search_fields = ('endpoint', 'user__username', 'ip_address')
    readonly_fields = (
        'user', 'endpoint', 'method', 'status_code',
        'ip_address', 'user_agent', 'response_time_ms', 'timestamp',
    )
    ordering = ['-timestamp']

    def method_badge(self, obj):
        colors = {'GET': '#16a34a', 'POST': '#2563eb', 'PUT': '#ca8a04', 'PATCH': '#0891b2', 'DELETE': '#dc2626'}
        color = colors.get(obj.method, '#6b7280')
        return format_html(
            '<span style="background:{};color:#fff;padding:2px 8px;border-radius:3px">{}</span>',
            color, obj.method,
        )
    method_badge.short_description = 'Method'

    def status_badge(self, obj):
        if obj.status_code < 300:
            color = '#16a34a'
        elif obj.status_code < 400:
            color = '#0891b2'
        elif obj.status_code < 500:
            color = '#ca8a04'
        else:
            color = '#dc2626'
        return format_html(
            '<span style="background:{};color:#fff;padding:2px 8px;border-radius:3px">{}</span>',
            color, obj.status_code,
        )
    status_badge.short_description = 'Status'

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(UserActivityLog)
class UserActivityLogAdmin(ModelAdmin):
    list_display  = ('created_at', 'action_badge', 'object_id', 'user', 'ip_address')
    list_filter   = ('action', 'object_type', 'created_at')
    search_fields = ('object_id', 'user__username', 'ip_address')
    readonly_fields = ('user', 'action', 'object_type', 'object_id', 'ip_address', 'metadata', 'created_at')
    ordering      = ['-created_at']

    def action_badge(self, obj):
        colors = {
            'view_attraction': '#1A4731',
            'view_region':     '#0891b2',
            'view_article':    '#7c3aed',
            'search':          '#ca8a04',
            'submit_review':   '#16a34a',
            'view_itinerary':  '#0e7490',
        }
        color = colors.get(obj.action, '#6b7280')
        return format_html(
            '<span style="background:{};color:#fff;padding:2px 8px;border-radius:3px;font-size:11px">{}</span>',
            color, obj.get_action_display(),
        )
    action_badge.short_description = 'Action'

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
