from rest_framework import serializers

from .models import Project, ProjectAttachment, ProjectMember

ALLOWED_ATTACHMENT_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg", ".doc", ".docx", ".xls", ".xlsx", ".txt", ".zip"}
MAX_ATTACHMENT_SIZE = 10 * 1024 * 1024


def validate_attachment_file(file):
    filename = file.name.lower()
    if not any(filename.endswith(extension) for extension in ALLOWED_ATTACHMENT_EXTENSIONS):
        raise serializers.ValidationError("Unsupported file type.")
    if file.size > MAX_ATTACHMENT_SIZE:
        raise serializers.ValidationError("Attachment size cannot exceed 10MB.")
    return file


class ProjectMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectMember
        fields = ["id", "project", "user", "role", "created_at"]
        read_only_fields = ["id", "created_at"]


class ProjectAttachmentSerializer(serializers.ModelSerializer):
    def validate_file(self, file):
        return validate_attachment_file(file)

    class Meta:
        model = ProjectAttachment
        fields = ["id", "project", "file", "original_name", "created_by", "created_at"]
        read_only_fields = ["id", "created_by", "created_at"]


class ProjectSerializer(serializers.ModelSerializer):
    memberships = ProjectMemberSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = [
            "id",
            "client",
            "name",
            "description",
            "status",
            "start_date",
            "due_date",
            "completed_at",
            "budget_amount",
            "memberships",
            "created_by",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_by", "created_at", "updated_at"]
