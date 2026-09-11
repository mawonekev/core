from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from unfold.admin import ModelAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(ModelAdmin, UserAdmin):
    list_display = ['username', 'email', 'full_name', 'role_badge', 'is_active', 'last_login', 'date_joined']
    list_filter = ['is_tour_operator', 'is_staff', 'is_active', 'is_superuser', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'phone']
    readonly_fields = ['last_login', 'date_joined']
    actions = ['deactivate_action', 'activate_action']

    fieldsets = (
        ('Account', {
            'fields': ('username', 'password'),
        }),
        ('Personal Info', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'bio'),
        }),
        ('Roles & Permissions', {
            'fields': (
                'is_active', 'is_tour_operator', 'is_staff', 'is_superuser',
                'groups', 'user_permissions',
            ),
        }),
        ('Timestamps', {
            'fields': ('last_login', 'date_joined'),
            'classes': ('collapse',),
        }),
    )

    add_fieldsets = (
        ('Create User', {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_tour_operator'),
        }),
    )

    def full_name(self, obj):
        return obj.get_full_name() or '—'
    full_name.short_description = 'Name'

    def role_badge(self, obj):
        if obj.is_superuser:
            return format_html('<span style="background:#7c3aed;color:#fff;padding:2px 8px;border-radius:3px;font-size:11px">Superuser</span>')
        if obj.is_staff:
            return format_html('<span style="background:#2563eb;color:#fff;padding:2px 8px;border-radius:3px;font-size:11px">Staff</span>')
        if obj.is_tour_operator:
            return format_html('<span style="background:#1A4731;color:#fff;padding:2px 8px;border-radius:3px;font-size:11px">Operator</span>')
        return format_html('<span style="background:#d1d5db;color:#374151;padding:2px 8px;border-radius:3px;font-size:11px">User</span>')
    role_badge.short_description = 'Role'

    def deactivate_action(self, request, queryset):
        updated = queryset.exclude(pk=request.user.pk).update(is_active=False)
        self.message_user(request, f'{updated} user(s) deactivated.')
    deactivate_action.short_description = 'Deactivate selected'

    def activate_action(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} user(s) activated.')
    activate_action.short_description = 'Activate selected'
