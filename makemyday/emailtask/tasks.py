from makemyday.celery import app
from celery.utils.log import get_task_logger

from .email import send_email

logger = get_task_logger(__name__)

@app.task(name="send_email_task")
def send_email_task(first_name, email, topic):
    logger.info("Sent reminder email")
    return send_email(first_name, email, topic)