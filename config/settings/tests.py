# flake8: noqa
from config.settings.base import *  # noqa
import os

DEBUG = True

SECRET_KEY = "yymxp*lpy_wuxbcc8zxduz9p(thzliu67zzwbe$o"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "DISABLE_SERVER_SIDE_CURSORS": True,
        "NAME": "marketplace-wendel",
        "USER": "postgres",
        "PASSWORD": "postgres",
        "HOST": "127.0.0.1",
        "PORT": "5432",
    }
}

STATIC_ROOT = BASE_DIR / "staticfiles"

STATIC_URL = "/static/"

STATICFILES_DIRS = [str(BASE_DIR / "static")]

MEDIA_ROOT = os.path.join(BASE_DIR, "static")
