from django.conf import settings
from django.db import models

from apps.accounts.models import ClientProfile
from apps.projects.models import Project
from common.models import CreatedByModel, TimeStampedModel


class Ticket(CreatedByModel):
    class Status(models.TextChoices):
        OPEN = "open", "Open"
        IN_PROGRESS = "in_progress", "In Progress"
        WAITING_ON_CLIENT = "waiting_on_client", "Waiting On Client"
        RESOLVED = "resolved", "Resolved"
        CLOSED = "closed", "Closed"

    class Priority(models.TextChoices):
        LOW = "low", "Low"
        MEDIUM = "medium", "Medium"
        HIGH = "high", "High"
        URGENT = "urgent", "Urgent"

    client = models.ForeignKey(ClientProfile, on_delete=models.PROTECT, related_name="tickets")
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, related_name="tickets", null=True, blank=True)
    subject = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=32, choices=Status.choices, default=Status.OPEN)
    priority = models.CharField(max_length=32, choices=Priority.choices, default=Priority.MEDIUM)
    ghl_contact_id = models.CharField(max_length=128, blank=True, db_index=True)
    source = models.CharField(max_length=64, default="portal")

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["client", "status"]),
            models.Index(fields=["priority", "status"]),
        ]

    def __str__(self):
        return self.subject


class TicketComment(TimeStampedModel):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="ticket_comments")
    message = models.TextField()
    is_internal = models.BooleanField(default=False)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Comment on {self.ticket_id}"
