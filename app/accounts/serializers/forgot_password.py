import re
import jwt

from django.contrib.auth import get_user_model

from rest_framework import serializers

from app.accounts.models import ResetPassword
from app.accounts.tasks import recovery_password, delete_token
from app.common import utils
from app.common import messages


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, attrs: dict) -> dict:
        request = self.context["request"]
        user = (
            get_user_model()
            .objects.filter(email__iexact=attrs.get("email"), is_active=True)
            .first()
        )
        if not user:
            raise serializers.ValidationError(
                {"message": messages.NOT_ALLOW_CHANGE_PASSWORD}
            )
        self.message = recovery_password(user, request)
        return attrs

    @property
    def data(self):
        return self.message


class ResetPasswordWithTokenSerializer(serializers.Serializer):
    token = serializers.CharField(write_only=True, min_length=32)
    password = serializers.CharField(write_only=True, min_length=6, max_length=20)

    def validate_token(self, data):
        try:
            token = utils.jwt_decode(data).get("token")
        except jwt.exceptions.DecodeError:
            raise serializers.ValidationError(messages.INVALID_TOKEN)

        if not re.match(r"([a-fA-F\d]{32})", token):
            raise serializers.ValidationError(messages.INVALID_TOKEN)

        token = ResetPassword.objects.filter(token=data).first()

        if not token:
            raise serializers.ValidationError(messages.INVALID_TOKEN)

        if token.is_invalid:
            token.delete()
            raise serializers.ValidationError(messages.TOKEN_EXPIRE)

        self.object_token = token
        return data

    def save(self, **kwargs):
        user = self.object_token.user
        if self.validated_data.get("token") == self.object_token.token:
            user.set_password(self.validated_data.get("password"))
            user.save(update_fields=["password", "updated_at"])
            delete_token.delay(self.object_token.pk)
        return user


class UserChangePasswordSerializer(serializers.ModelSerializer):
    password_old = serializers.CharField(write_only=True, min_length=6)
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = get_user_model()
        fields = ("password", "password_old")

    def validate(self, data):
        if not self.instance.check_password(data.get("password_old")):
            raise serializers.ValidationError(messages.CURRENT_PASSWORD_INVALID)
        return data

    def update(self, instance, validated_data):
        instance.set_password(validated_data.get("password"))
        instance.save()
        return instance
