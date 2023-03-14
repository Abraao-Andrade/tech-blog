from django.utils import timezone
from django.conf import settings

from config.celery import app
from celery.utils.log import get_task_logger

from app.accounts.models import ResetPassword, User
from app.common import messages
from app.common import utils
from app.common.active_campaign import ActiveCampaign

logger = get_task_logger(__name__)

active_campaign = ActiveCampaign()


def recovery_password(user, request):
    token = ResetPassword().generation_token(user, request)
    diff_seconds = (timezone.now() - token.updated_at).total_seconds()
    email = user.email
    message = messages.EMAIL_CHANGE_INSTRUCTION.format(email=email)

    if not (diff_seconds // 60) >= 10 and token.sending_attempts > 0:
        message = messages.RATE_LIMIT_CHANGE_PASSWORD
        status = 404
    else:
        status = 200
        token.incr_attempts()
        recovery_url = f"https://{settings.DOMAIN}/reset-password?token={token.token}"
        email_recovery_password.delay(user.email, recovery_url)

    return {"message": message, "status": status}


@app.task(queue=settings.CELERY_DEFAULT_QUEUE)
def email_recovery_password(user, recovery_url):
    """
    Recovery password name, email and token
    """
    try:
        user = User.objects.filter(email__iexact=user).first()
        contact_id = user.create_or_get_contact_id
        active_campaign.update_custom_field(
            contact_id, recovery_url, "recovery_url_link"
        )
        active_campaign.add_tag_to_contact(contact_id, "recovery_password")
    except Exception as e:
        logger.error(f"[email_recovery_password] error {e}")
    return


@app.task(queue=settings.CELERY_DEFAULT_QUEUE)
def email_first_access(user, password):
    """
    First access send name and email
    """
    try:
        user = User.objects.filter(email__iexact=user).first()
        contact_id = user.create_or_get_contact_id
        active_campaign.update_custom_field(contact_id, password, "password")
        active_campaign.add_tag_to_contact(contact_id, "first_access")
    except Exception as e:
        logger.error(f"[email_first_access] error as {e}")


@app.task(queue=settings.CELERY_DEFAULT_QUEUE)
def delete_token(token_id: int) -> None:
    reset_password = ResetPassword.objects.get(pk=token_id)
    reset_password.create_history()
    reset_password.delete()


@app.task(queue=settings.CELERY_DEFAULT_QUEUE)
def generation_password(user_id: int):
    user = User.objects.get(pk=user_id)
    passwd = utils.random_password()
    user.set_password(passwd)
    user.save()
    try:
        contact_id = user.create_or_get_contact_id
        active_campaign.update_custom_field(contact_id, passwd, "password")
        active_campaign.add_tag_to_contact(contact_id, "generation_password")
    except Exception as e:
        logger.error(f"[generation_password] error as {e}")
