from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from common.permissions import IsAdminRole

from .models import ClientProfile, User
from .permissions import IsAdminOrSelf
from .serializers import ClientProfileSerializer, UserCreateSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        user = self.request.user
        queryset = User.objects.all().order_by("email")
        if user.role == User.Role.ADMIN:
            return queryset
        if user.role == User.Role.TEAM_MEMBER:
            return queryset.filter(role__in=[User.Role.ADMIN, User.Role.TEAM_MEMBER], is_active=True)
        return queryset.filter(id=user.id)

    def get_serializer_class(self):
        if self.action == "create":
            return UserCreateSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action == "me":
            return [permissions.IsAuthenticated()]
        if self.action in ["create", "destroy"]:
            return [IsAdminRole()]
        if self.action == "list":
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated(), IsAdminOrSelf()]

    @action(detail=False, methods=["get"])
    def me(self, request):
        return Response(UserSerializer(request.user, context={"request": request}).data)


class ClientProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ClientProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAdminRole()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        queryset = ClientProfile.objects.select_related("user").order_by("company_name")
        if user.role == User.Role.ADMIN:
            return queryset
        if user.role == User.Role.CLIENT:
            return queryset.filter(user=user)
        return queryset.filter(is_active=True)
