import posixpath
import uuid
import base64
from datetime import datetime

from django.core.files.base import ContentFile
from django.core.files.utils import validate_file_name
from django.db import models

from rest_framework.fields import SkipField
from rest_framework import serializers


class FileField(models.FileField):
    def generate_filename(self, instance, filename):
        ext = filename.split(".")[-1]
        hash_name = str(uuid.uuid4())
        filename = f"{hash_name}.{ext}"
        upload_to = f"{self.upload_to}/%Y/%m/%d/"
        dirname = datetime.now().strftime(upload_to)
        filename = posixpath.join(dirname, filename)
        filename = validate_file_name(filename, allow_relative_path=True)
        return self.storage.generate_filename(filename)


class ImageField(models.ImageField):
    def generate_filename(self, instance, filename):
        ext = filename.split(".")[-1]
        hash_name = str(uuid.uuid4())
        filename = f"{hash_name}.{ext}"
        upload_to = f"{self.upload_to}/%Y/%m/%d/"
        dirname = datetime.now().strftime(upload_to)
        filename = posixpath.join(dirname, filename)
        filename = validate_file_name(filename, allow_relative_path=True)
        return self.storage.generate_filename(filename)


class Base64FieldMixin(object):
    def _decode(self, data):
        if isinstance(data, str) and data.startswith("data:"):
            # base64 encoded file - decode
            format, datastr = data.split(";base64,")  # format ~= data:image/X,
            ext = format.split("/")[-1]  # guess file extension
            if ext[:3] == "svg":
                ext = "svg"

            data = ContentFile(
                base64.b64decode(datastr), name="{}.{}".format(uuid.uuid4(), ext)
            )

        elif isinstance(data, str) and data.startswith("http"):
            raise SkipField()
        return data

    def to_internal_value(self, data):
        data = self._decode(data)
        file_object = super().to_internal_value(data)
        django_field = self._DjangoImageField()
        django_field.error_messages = self.error_messages
        return django_field.clean(file_object)


class Base64ImageField(Base64FieldMixin, serializers.ImageField):
    pass


class Base64FileField(Base64FieldMixin, serializers.FileField):
    pass
