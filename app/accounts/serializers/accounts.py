from django.contrib.auth import authenticate

from rest_framework import serializers
from app.common.fields import Base64ImageField

from app.accounts.models import Customer, User
from app.common.messages import (
    DUPLICATION_EMAIL,
    INVALID_PASSWORD_OR_USER,
    BAD_CONFIRM_PASSWORD,
)


class AccountSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    phone = serializers.CharField(required=False)
    photo = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = [
            "name",
            "last_name",
            "email",
            "phone",
            "birth_date",
            "city",
            "state",
            "address",
            "number",
            "district",
            "complement",
            "zipcode",
            "photo",
            "token",
            "created_at",
            "last_login",
            "is_active",
        ]
        read_only_fields = ["token", "created_at", "last_login", "agreed"]

    def create(self, validated_data: dict):
        validated_data["request"] = self.context["request"]

        if self.Meta.model.objects.filter(email=validated_data.get("email")).exists():
            raise serializers.ValidationError({"email": [DUPLICATION_EMAIL]})
        return self.Meta.model.objects.create_user(**validated_data)


class AccountCreateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)
    phone = serializers.CharField(required=False)
    photo = Base64ImageField(required=False, allow_null=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = Customer
        fields = [
            "name",
            "last_name",
            "email",
            "phone",
            "photo",
            "password",
            "token",
        ]
        read_only_fields = ["token", "created_at", "last_login", "agreed"]

    def create(self, validated_data: dict):
        validated_data["request"] = self.context["request"]

        if self.Meta.model.objects.filter(email=validated_data.get("email")).exists():
            raise serializers.ValidationError({"email": [DUPLICATION_EMAIL]})
        user = self.Meta.model.objects.create_user(**validated_data)
        return user


class SignInSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs: dict):
        request = self.context.get("request")
        user = authenticate(request, **attrs)

        if not user:
            raise serializers.ValidationError({"message": INVALID_PASSWORD_OR_USER})
        self.user = user
        return user

    @property
    def data(self) -> dict:
        return {
            "id": self.user.id,
            "name": self.user.name,
            "last_name": self.user.last_name,
            "email": self.user.email,
            "phone": self.user.phone,
            "birth_date": self.user.birth_date,
            "agreed": self.user.agreed,
            "token": self.user.token,
            "refresh": self.user.refresh,
            "created_at": self.user.created_at,
            "last_login": self.user.last_login,
        }


class UserInfoSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    agreed = serializers.BooleanField(read_only=True)

    class Meta:
        model = Customer
        fields = [
            "id",
            "name",
            "last_name",
            "phone",
            "email",
            "photo",
            "refresh",
            "created_at",
            "last_login",
            "agreed",
            "birth_date",
            "city",
            "state",
            "address",
            "number",
            "district",
            "complement",
            "zipcode",
            "is_active",
        ]


class SimpleUserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            "id",
            "name",
            "last_name",
            "phone",
            "email",
            "photo",
            "created_at",
        ]


class UserChangePasswordSerializer(serializers.ModelSerializer):
    password_old = serializers.CharField(write_only=True, min_length=6)
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ("password", "password_old")

    def validate(self, data):
        if not self.instance.check_password(data.get("password_old")):
            raise serializers.ValidationError({"password": [BAD_CONFIRM_PASSWORD]})
        return data

    def update(self, instance, validated_data):
        instance.set_password(validated_data.get("password"))
        instance.save(update_fields=["password", "updated_at"])
        return instance
