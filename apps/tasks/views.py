from django.utils import timezone
from rest_framework import exceptions, permissions, viewsets

from apps.accounts.models import User

from .models import Task, TaskAttachment
from .serializers import TaskAttachmentSerializer, TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Task.objects.select_related("project", "assignee", "created_by", "parent_task")

        if user.role == User.Role.ADMIN:
            scoped_queryset = queryset
        elif user.role == User.Role.CLIENT:
            scoped_queryset = queryset.filter(project__client__user=user)
        else:
            scoped_queryset = queryset.filter(project__memberships__user=user).distinct()

        project_id = self.request.query_params.get("project")
        if project_id:
            scoped_queryset = scoped_queryset.filter(project_id=project_id)

        parent_task_id = self.request.query_params.get("parent_task")
        top_level = self.request.query_params.get("top_level")
        if parent_task_id:
            scoped_queryset = scoped_queryset.filter(parent_task_id=parent_task_id)
        elif top_level in ["1", "true", "True"]:
            scoped_queryset = scoped_queryset.filter(parent_task__isnull=True)

        return scoped_queryset

    def perform_create(self, serializer):
        if self.request.user.role == User.Role.CLIENT:
            raise exceptions.PermissionDenied("Clients cannot create tasks.")
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        if self.request.user.role == User.Role.CLIENT:
            raise exceptions.PermissionDenied("Clients cannot update tasks.")

        status = serializer.validated_data.get("status")
        if status == Task.Status.COMPLETED and not serializer.instance.completed_at:
            serializer.save(completed_at=timezone.now())
            return
        if status and status != Task.Status.COMPLETED:
            serializer.save(completed_at=None)
            return

        serializer.save()


class TaskAttachmentViewSet(viewsets.ModelViewSet):
    serializer_class = TaskAttachmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = TaskAttachment.objects.select_related("task", "created_by")
        if user.role == User.Role.ADMIN:
            scoped_queryset = queryset
        elif user.role == User.Role.CLIENT:
            scoped_queryset = queryset.filter(task__project__client__user=user)
        else:
            scoped_queryset = queryset.filter(task__project__memberships__user=user).distinct()

        task_id = self.request.query_params.get("task")
        if task_id:
            scoped_queryset = scoped_queryset.filter(task_id=task_id)

        return scoped_queryset

    def perform_create(self, serializer):
        if self.request.user.role == User.Role.CLIENT:
            raise exceptions.PermissionDenied("Clients cannot upload task attachments.")

        task = serializer.validated_data["task"]
        if self.request.user.role != User.Role.ADMIN and not task.project.memberships.filter(user=self.request.user).exists():
            raise exceptions.PermissionDenied("You cannot upload attachments to this task.")

        file = serializer.validated_data.get("file")
        serializer.save(created_by=self.request.user, original_name=file.name if file else "")
