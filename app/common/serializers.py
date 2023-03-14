from django.db import models

from rest_framework.serializers import (
    ModelSerializer as DRFModelSerializer,
)

from .fields import Base64FileField, Base64ImageField


class Base64ModelSerializerMixin:
    def __init__(self, *args, **kwargs):
        self.serializer_field_mapping.update(
            {
                models.FileField: Base64FileField,
                models.ImageField: Base64ImageField,
            }
        )
        super().__init__(*args, **kwargs)


class ModelSerializer(Base64ModelSerializerMixin, DRFModelSerializer):
    pass
