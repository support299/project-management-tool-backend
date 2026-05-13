from rest_framework import exceptions, permissions, serializers, viewsets

from apps.accounts.models import User

from .models import Ticket, TicketComment
from .serializers import TicketCommentSerializer, TicketSerializer


class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Ticket.objects.select_related("client", "project", "created_by").prefetch_related("comments")
        if user.role == User.Role.ADMIN:
            scoped_queryset = queryset
        elif user.role == User.Role.CLIENT:
            scoped_queryset = queryset.filter(client__user=user)
        else:
            scoped_queryset = queryset.filter(project__memberships__user=user).distinct()

        project_id = self.request.query_params.get("project")
        if project_id:
            scoped_queryset = scoped_queryset.filter(project_id=project_id)

        return scoped_queryset

    def perform_create(self, serializer):
        user = self.request.user
        if user.role == User.Role.CLIENT:
            client_profile = getattr(user, "client_profile", None)
            if not client_profile:
                raise serializers.ValidationError("Client users need a client profile before creating tickets.")
            serializer.save(created_by=user, client=client_profile)
            return
        if not serializer.validated_data.get("client"):
            raise serializers.ValidationError({"client": "This field is required."})
        serializer.save(created_by=user)

    def perform_update(self, serializer):
        if self.request.user.role == User.Role.CLIENT:
            raise exceptions.PermissionDenied("Clients cannot update tickets.")
        serializer.save()


class TicketCommentViewSet(viewsets.ModelViewSet):
    serializer_class = TicketCommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = TicketComment.objects.select_related("ticket", "author")
        if user.role == User.Role.ADMIN:
            scoped_queryset = queryset
        elif user.role == User.Role.CLIENT:
            scoped_queryset = queryset.filter(ticket__client__user=user, is_internal=False)
        else:
            scoped_queryset = queryset.filter(ticket__project__memberships__user=user).distinct()

        ticket_id = self.request.query_params.get("ticket")
        if ticket_id:
            scoped_queryset = scoped_queryset.filter(ticket_id=ticket_id)

        return scoped_queryset

    def perform_create(self, serializer):
        user = self.request.user
        ticket = serializer.validated_data["ticket"]

        if user.role == User.Role.ADMIN:
            serializer.save(author=user)
            return

        if user.role == User.Role.CLIENT:
            if getattr(ticket.client, "user_id", None) != user.id:
                raise exceptions.PermissionDenied("You cannot comment on this ticket.")
            serializer.save(author=user, is_internal=False)
            return

        if not ticket.project_id or not ticket.project.memberships.filter(user=user).exists():
            raise exceptions.PermissionDenied("You cannot comment on this ticket.")
        serializer.save(author=user)
