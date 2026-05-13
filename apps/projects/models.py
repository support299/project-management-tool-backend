from django.conf import settings
from django.db import models

from apps.accounts.models import ClientProfile
from common.models import CreatedByModel, TimeStampedModel


class Project(CreatedByModel):
    class Status(models.TextChoices):
        PLANNING = "planning", "Planning"
        ACTIVE = "active", "Active"
        ON_HOLD = "on_hold", "On Hold"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"

    client = models.ForeignKey(ClientProfile, on_delete=models.PROTECT, related_name="projects")
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=32, choices=Status.choices, default=Status.PLANNING)
    start_date = models.DateField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    budget_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["client", "status"]),
            models.Index(fields=["due_date"]),
        ]

    def __str__(self):
        return self.name


class ProjectMember(TimeStampedModel):
    class Role(models.TextChoices):
        OWNER = "owner", "Owner"
        MANAGER = "manager", "Manager"
        MEMBER = "member", "Member"

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="memberships")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="project_memberships")
    role = models.CharField(max_length=32, choices=Role.choices, default=Role.MEMBER)

    class Meta:
        unique_together = ("project", "user")

    def __str__(self):
        return f"{self.user} - {self.project}"


class ProjectAttachment(CreatedByModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="attachments")
    file = models.FileField(upload_to="project_attachments/")
    original_name = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.original_name or self.file.name
