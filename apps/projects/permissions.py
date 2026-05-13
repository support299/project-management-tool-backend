from rest_framework.permissions import SAFE_METHODS, BasePermission


class ProjectAccessPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.role == "admin":
            return True
        if user.role == "client":
            return getattr(obj.client, "user_id", None) == user.id and request.method in SAFE_METHODS
        return obj.memberships.filter(user=user).exists()
