from django.conf import settings
from django.db import models

from common.models import TimeStampedModel


class Notification(TimeStampedModel):
    class Type(models.TextChoices):
        TASK_ASSIGNED = "task_assigned", "Task Assigned"
        TICKET_UPDATED = "ticket_updated", "Ticket Updated"
        PROJECT_UPDATED = "project_updated", "Project Updated"
        SYSTEM = "system", "System"

    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")
    notification_type = models.CharField(max_length=64, choices=Type.choices)
    title = models.CharField(max_length=255)
    message = models.TextField(blank=True)
    related_object_type = models.CharField(max_length=100, blank=True)
    related_object_id = models.PositiveBigIntegerField(null=True, blank=True)
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["recipient", "is_read"]),
            models.Index(fields=["related_object_type", "related_object_id"]),
        ]

    def __str__(self):
        return self.title
