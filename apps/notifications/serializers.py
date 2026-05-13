from rest_framework import serializers

from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            "id",
            "recipient",
            "notification_type",
            "title",
            "message",
            "related_object_type",
            "related_object_id",
            "is_read",
            "read_at",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "recipient", "created_at", "updated_at"]
