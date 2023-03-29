from config.celery import app
from django.conf import settings
from celery.utils.log import get_task_logger

from .models import Article

logger = get_task_logger(__name__)


@app.task(queue=settings.CELERY_DEFAULT_QUEUE)
def handle_update_article_read_count(article_id: int):
    try:
        if article := Article.objects.get(pk=article_id):
            article.read_count += 1
            article.save()
    except Exception as e:
        logger.error(
            f"[handle_update_article_read_count] Error in update article read count response {e}"
        )
