from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.notifications.services import create_task_assignment_notification

from .models import Task


@receiver(post_save, sender=Task)
def notify_assignee_on_task_create(sender, instance, created, **kwargs):
    if created and instance.assignee_id:
        create_task_assignment_notification(instance)
