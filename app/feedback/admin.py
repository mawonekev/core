from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin

from .models import Review, UserFeedback


@admin.register(UserFeedback)
class UserFeedbackAdmin(ModelAdmin):
    list_display = ['subject', 'feedback_type', 'status_badge', 'name', 'email', 'created_at']
    list_filter = ['feedback_type', 'status', 'created_at']
    search_fields = ['subject', 'message', 'name', 'email']
    readonly_fields = ['created_at', 'updated_at', 'ip_address', 'user_agent', 'user']

    fieldsets = (
        ('Message', {
            'fields': ('feedback_type', 'subject', 'message', 'rating', 'attachment'),
        }),
        ('Sender', {
            'fields': ('user', 'name', 'email'),
        }),
        ('Admin Response', {
            'fields': ('status', 'response'),
        }),
        ('Meta', {
            'fields': ('ip_address', 'user_agent', 'content_type', 'object_id'),
            'classes': ('collapse',),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    def status_badge(self, obj):
        colours = {
            'pending': '#ca8a04',
            'in_review': '#2563eb',
            'resolved': '#16a34a',
            'closed': '#6b7280',
        }
        colour = colours.get(obj.status, '#6b7280')
        return format_html(
            '<span style="background:{};color:#fff;padding:2px 8px;border-radius:3px">{}</span>',
            colour, obj.get_status_display()
        )
    status_badge.short_description = 'Status'


@admin.register(Review)
class ReviewAdmin(ModelAdmin):
    list_display = ['attraction', 'reviewer_name', 'rating_stars', 'approval_badge', 'is_flagged', 'created_at']
    list_filter = ['is_approved', 'is_flagged', 'rating', 'visit_type', 'created_at']
    search_fields = ['body', 'reviewer_name', 'attraction__name']
    readonly_fields = ['created_at', 'updated_at', 'helpful_count', 'user']
    actions = ['approve_action', 'reject_action', 'flag_action']

    fieldsets = (
        ('Review', {
            'fields': ('attraction', 'rating', 'body'),
        }),
        ('Reviewer', {
            'fields': ('user', 'reviewer_name', 'reviewer_email', 'reviewer_country'),
        }),
        ('Visit Context', {
            'fields': ('visit_type', 'visit_season', 'visited_at'),
            'classes': ('collapse',),
        }),
        ('Sub-ratings', {
            'fields': ('rating_scenery', 'rating_accessibility', 'rating_value_for_money', 'rating_safety', 'rating_facilities'),
            'classes': ('collapse',),
        }),
        ('Moderation', {
            'fields': ('is_approved', 'is_flagged', 'helpful_count'),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    def rating_stars(self, obj):
        filled = '★' * obj.rating
        empty = '☆' * (5 - obj.rating)
        return format_html('<span style="color:#f59e0b;font-size:14px">{}</span><span style="color:#d1d5db;font-size:14px">{}</span>', filled, empty)
    rating_stars.short_description = 'Rating'

    def approval_badge(self, obj):
        if obj.is_approved:
            return format_html('<span style="background:#16a34a;color:#fff;padding:2px 8px;border-radius:3px">Approved</span>')
        return format_html('<span style="background:#ca8a04;color:#fff;padding:2px 8px;border-radius:3px">Pending</span>')
    approval_badge.short_description = 'Approval'

    def approve_action(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, f'{queryset.count()} review(s) approved.')
    approve_action.short_description = 'Approve selected'

    def reject_action(self, request, queryset):
        queryset.update(is_approved=False)
        self.message_user(request, f'{queryset.count()} review(s) rejected.')
    reject_action.short_description = 'Reject selected'

    def flag_action(self, request, queryset):
        queryset.update(is_flagged=True)
        self.message_user(request, f'{queryset.count()} review(s) flagged.')
    flag_action.short_description = 'Flag selected'
