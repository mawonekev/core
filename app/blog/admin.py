from django.contrib import admin
from django.db import models
from django.utils.html import format_html
from django_ckeditor_5.widgets import CKEditor5Widget
from unfold.admin import ModelAdmin

from .models import Article


@admin.register(Article)
class ArticleAdmin(ModelAdmin):
    list_display = ['title', 'author', 'publish_badge', 'approval_badge', 'status_badge', 'published_at', 'created_at']
    list_filter = ['status', 'is_approved', 'deleted_at', 'created_at']
    search_fields = ['title', 'excerpt', 'content', 'tags']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['related_attractions']
    readonly_fields = ['created_at', 'updated_at', 'deleted_at']
    actions = ['approve_action', 'reject_action', 'restore_action', 'soft_delete_action']

    formfield_overrides = {
        models.TextField: {'widget': CKEditor5Widget(config_name='default')},
    }

    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'excerpt', 'content', 'featured_image', 'image_alt', 'tags'),
        }),
        ('Related Attractions', {
            'fields': ('related_attractions',),
        }),
        ('Publishing', {
            'fields': ('author', 'status', 'published_at'),
        }),
        ('Moderation', {
            'fields': ('is_approved', 'deleted_at'),
        }),
        ('SEO', {
            'fields': (
                'meta_title', 'meta_description', 'meta_keywords',
                'og_title', 'og_description', 'og_image',
                'canonical_url', 'no_index',
                'sitemap_priority', 'sitemap_changefreq',
            ),
            'classes': ('collapse',),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    def publish_badge(self, obj):
        colors = {'draft': '#6b7280', 'published': '#16a34a', 'archived': '#dc2626'}
        color = colors.get(obj.status, '#6b7280')
        return format_html(
            '<span style="background:{};color:#fff;padding:2px 8px;border-radius:3px;font-size:11px">{}</span>',
            color, obj.get_status_display()
        )
    publish_badge.short_description = 'Publish'

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
        self.message_user(request, f'{queryset.count()} article(s) approved.')
    approve_action.short_description = 'Approve selected'

    def reject_action(self, request, queryset):
        queryset.update(is_approved=False)
        self.message_user(request, f'{queryset.count()} article(s) rejected.')
    reject_action.short_description = 'Reject selected'

    def restore_action(self, request, queryset):
        queryset.update(deleted_at=None)
        self.message_user(request, f'{queryset.count()} article(s) restored.')
    restore_action.short_description = 'Restore deleted'

    def soft_delete_action(self, request, queryset):
        for obj in queryset:
            obj.delete()
        self.message_user(request, f'{queryset.count()} article(s) moved to trash.')
    soft_delete_action.short_description = 'Move to trash'
