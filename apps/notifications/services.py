from .models import Notification


def create_task_assignment_notification(task):
    return Notification.objects.create(
        recipient=task.assignee,
        notification_type=Notification.Type.TASK_ASSIGNED,
        title="New task assigned",
        message=f"You have been assigned to: {task.title}",
        related_object_type="task",
        related_object_id=task.id,
    )
