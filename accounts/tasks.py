from celery import current_app
from accounts.emails import send_email_activation_code
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@current_app.task(name="send_email_activation_code_task")
def send_email_activation_code_task(full_name, email, activate_code_url):
    logger.info("Send email activate code")
    send_email_activation_code(full_name, email, activate_code_url)
