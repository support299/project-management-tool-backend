from django.utils import timezone
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Notification
from .serializers import NotificationSerializer


class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "patch", "delete", "post", "head", "options"]

    def get_queryset(self):
        queryset = Notification.objects.filter(recipient=self.request.user)
        is_read = self.request.query_params.get("is_read")
        if is_read in ["true", "True", "1"]:
            return queryset.filter(is_read=True)
        if is_read in ["false", "False", "0"]:
            return queryset.filter(is_read=False)
        return queryset

    @action(detail=True, methods=["post"])
    def mark_read(self, request, pk=None):
        notification = self.get_object()
        notification.is_read = True
        notification.read_at = timezone.now()
        notification.save(update_fields=["is_read", "read_at", "updated_at"])
        return Response(self.get_serializer(notification).data)
