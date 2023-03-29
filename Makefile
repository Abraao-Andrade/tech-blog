celery:
	DJANGO_SETTINGS_MODULE='config.settings.local' celery -A config worker -lINFO -Q blog-backend -E --concurrency=1