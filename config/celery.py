from __future__ import absolute_import
import os

from django.apps import apps
from django.conf import settings

from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
QUEUE_NAME = settings.CELERY_DEFAULT_QUEUE

app = Celery(QUEUE_NAME)

if settings.DEBUG:
    app.conf.worker_cancel_long_running_tasks_on_connection_loss = True

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(lambda: [n.name for n in apps.get_app_configs()])
