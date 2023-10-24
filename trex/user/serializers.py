from rest_framework import serializers

from core.utils import response_payload
from .models import User


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "role",
            "first_name",
            "last_name",
        )


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "role",
            "first_name",
            "last_name",
            "gender",
            "avatar",
        )


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "role",
            "first_name",
            "last_name",
            "gender",
            "avatar",
        )
        read_only_fields = (
            "id",
            "username",
            "email",
            "role",
        )


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "password",
            "password2",
            "role",
            "first_name",
            "last_name",
            "gender",
            "avatar",
        )
        read_only_fields = (
            "id",
        )

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                detail="A user with that email already exists",
            )
        return email

    def validate_password(self, password):
        password2 = self.get_initial().get("password2")
        if password != password2:
            raise serializers.ValidationError(
                detail="Passwords do not match"
            )
        return password

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('password2')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.is_active = True
        user.save()
        return user

    def to_representation(self, instance):
        return UserDetailSerializer(instance).data
