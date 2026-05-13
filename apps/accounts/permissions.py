from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrSelf(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.role == "admin":
            return True
        return obj == request.user and request.method in SAFE_METHODS
