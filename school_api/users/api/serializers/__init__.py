from django.contrib.auth.hashers import make_password
from djoser.serializers import UserCreateSerializer
from djoser.serializers import UserSerializer as DjoseruserSerializer
from rest_framework import serializers

from school_api.users import settings as app_settings
from school_api.users.models import User


class CustomUserSerializer(DjoseruserSerializer):
    class Meta:
        model = User
        fields = ["username", "name", "role", "is_active"]


class CustomUserCreateSerializer(UserCreateSerializer):
    role = serializers.CharField(required=True)
    name = serializers.CharField(required=True)
    username = serializers.CharField(required=True)
    is_active = serializers.ReadOnlyField()

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ("name", "username", "password", "role", "is_active")

    def validate_role(self, value):
        if value not in ["librarian", "student"]:
            raise serializers.ValidationError(app_settings.MSG_INVALID_ROLE)

        return value

    def validate(self, attrs):
        """override"""
        if attrs.get("name"):
            full_name_split = attrs.pop("name").strip().split(" ", 1)
            attrs["first_name"] = full_name_split.pop(0)
            attrs["last_name"] = full_name_split.pop(0) if full_name_split else ""

        data = super().validate(attrs)
        data["password"] = make_password(data["password"])
        return data

    def perform_create(self, validated_data):
        validated_data["is_staff"] = False
        validated_data["is_superuser"] = False
        user = User.objects.create(**validated_data)

        return user
