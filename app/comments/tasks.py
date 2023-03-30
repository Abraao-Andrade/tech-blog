from config.celery import app
from django.conf import settings
from celery.utils.log import get_task_logger

from .models import Comment

logger = get_task_logger(__name__)


@app.task(queue=settings.CELERY_DEFAULT_QUEUE)
def handle_update_comment_interaction(comment_id: int, like: bool, spam: bool):
    try:
        if comment := Comment.objects.get(pk=comment_id):
            if like:
                comment.like += 1
                comment.save()
            if spam:
                comment.spam += 1
                comment.save()
    except Exception as e:
        logger.error(
            f"[handle_update_comment_interaction] Error in update comment interaction response {e}"
        )
