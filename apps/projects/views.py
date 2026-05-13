from rest_framework import exceptions, permissions, viewsets

from apps.accounts.models import User
from common.permissions import IsAdminRole

from .models import Project, ProjectAttachment, ProjectMember
from .permissions import ProjectAccessPermission
from .serializers import ProjectAttachmentSerializer, ProjectMemberSerializer, ProjectSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, ProjectAccessPermission]

    def get_queryset(self):
        user = self.request.user
        queryset = Project.objects.select_related("client", "created_by").prefetch_related("memberships")

        if user.role == User.Role.ADMIN:
            return queryset
        if user.role == User.Role.CLIENT:
            return queryset.filter(client__user=user)
        return queryset.filter(memberships__user=user).distinct()

    def perform_create(self, serializer):
        if self.request.user.role != User.Role.ADMIN:
            raise exceptions.PermissionDenied("Only admins can create projects.")
        serializer.save(created_by=self.request.user)


class ProjectMemberViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectMemberSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAdminRole()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        queryset = ProjectMember.objects.select_related("project", "user")
        if user.role == User.Role.ADMIN:
            return queryset
        return queryset.filter(project__memberships__user=user).distinct()


class ProjectAttachmentViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectAttachmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = ProjectAttachment.objects.select_related("project", "created_by")
        if user.role == User.Role.ADMIN:
            scoped_queryset = queryset
        elif user.role == User.Role.CLIENT:
            scoped_queryset = queryset.filter(project__client__user=user)
        else:
            scoped_queryset = queryset.filter(project__memberships__user=user).distinct()

        project_id = self.request.query_params.get("project")
        if project_id:
            scoped_queryset = scoped_queryset.filter(project_id=project_id)

        return scoped_queryset

    def perform_create(self, serializer):
        if self.request.user.role == User.Role.CLIENT:
            raise exceptions.PermissionDenied("Clients cannot upload project attachments.")

        project = serializer.validated_data["project"]
        if self.request.user.role != User.Role.ADMIN and not project.memberships.filter(user=self.request.user).exists():
            raise exceptions.PermissionDenied("You cannot upload attachments to this project.")

        file = serializer.validated_data.get("file")
        serializer.save(created_by=self.request.user, original_name=file.name if file else "")
