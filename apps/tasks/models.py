from django.conf import settings
from django.db import models

from apps.projects.models import Project
from common.models import CreatedByModel


class Task(CreatedByModel):
    class Status(models.TextChoices):
        TODO = "todo", "To Do"
        IN_PROGRESS = "in_progress", "In Progress"
        BLOCKED = "blocked", "Blocked"
        REVIEW = "review", "Review"
        COMPLETED = "completed", "Completed"

    class Priority(models.TextChoices):
        LOW = "low", "Low"
        MEDIUM = "medium", "Medium"
        HIGH = "high", "High"
        URGENT = "urgent", "Urgent"

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")
    parent_task = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="subtasks",
        null=True,
        blank=True,
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="assigned_tasks",
        null=True,
        blank=True,
    )
    status = models.CharField(max_length=32, choices=Status.choices, default=Status.TODO)
    priority = models.CharField(max_length=32, choices=Priority.choices, default=Priority.MEDIUM)
    start_date = models.DateField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["due_date", "-created_at"]
        indexes = [
            models.Index(fields=["project", "status"]),
            models.Index(fields=["assignee", "status"]),
            models.Index(fields=["due_date"]),
        ]

    def __str__(self):
        return self.title


class TaskAttachment(CreatedByModel):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="attachments")
    file = models.FileField(upload_to="task_attachments/")
    original_name = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.original_name or self.file.name
