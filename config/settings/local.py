# flake8: noqa
from .base import *
import os

STATIC_ROOT = BASE_DIR / "staticfiles"

STATIC_URL = "/static/"

STATICFILES_DIRS = [str(BASE_DIR / "static")]

MEDIA_ROOT = os.path.join(BASE_DIR, "static")
