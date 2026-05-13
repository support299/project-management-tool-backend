from rest_framework import serializers

from .models import Ticket, TicketComment


class TicketCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketComment
        fields = ["id", "ticket", "author", "message", "is_internal", "created_at", "updated_at"]
        read_only_fields = ["id", "author", "created_at", "updated_at"]


class TicketSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()

    def get_comments(self, obj):
        request = self.context.get("request")
        comments = obj.comments.all()
        if request and request.user.role == "client":
            comments = comments.filter(is_internal=False)
        return TicketCommentSerializer(comments, many=True, context=self.context).data

    class Meta:
        model = Ticket
        fields = [
            "id",
            "client",
            "project",
            "subject",
            "description",
            "status",
            "priority",
            "ghl_contact_id",
            "source",
            "comments",
            "created_by",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_by", "created_at", "updated_at"]
        extra_kwargs = {
            "client": {"required": False},
        }
