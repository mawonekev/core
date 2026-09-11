from rest_framework import permissions


class ReadOnlyOrAdmin(permissions.BasePermission):
    # public can read, only admin/staff can write
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and (request.user.is_staff or request.user.is_superuser)

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and (request.user.is_staff or request.user.is_superuser)


class IsEmailVerified(permissions.BasePermission):
    message = 'Please verify your email address first.'

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return getattr(request.user, 'is_email_verified', False)
