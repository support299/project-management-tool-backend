from rest_framework import serializers

from .models import ClientProfile, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "role",
            "phone",
            "avatar",
            "is_active",
            "date_joined",
        ]
        read_only_fields = ["id", "date_joined"]


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["id", "email", "password", "first_name", "last_name", "role", "phone"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        return User.objects.create_user(password=password, **validated_data)


class ClientProfileSerializer(serializers.ModelSerializer):
    def validate_user(self, user):
        if not user:
            return user

        if user.role != User.Role.CLIENT:
            raise serializers.ValidationError("Only client users can be linked to a client profile.")

        existing_profile = getattr(user, "client_profile", None)
        if existing_profile and existing_profile != self.instance:
            raise serializers.ValidationError("This user is already linked to another client profile.")

        return user

    class Meta:
        model = ClientProfile
        fields = [
            "id",
            "user",
            "company_name",
            "contact_name",
            "email",
            "phone",
            "ghl_contact_id",
            "notes",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
