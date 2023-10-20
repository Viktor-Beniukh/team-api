from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        """Splitting Permissions between Administrator and Anonymous User"""
        return bool(
            request.method in SAFE_METHODS
            or request.user
            and request.user.is_staff
        )
