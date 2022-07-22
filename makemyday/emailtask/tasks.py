from makemyday.celery import app
from celery.utils.log import get_task_logger
from main.models import Notification
from questions.models import Response
from .email import send_email

logger = get_task_logger(__name__)

@app.task(name="send_email_task")
def send_email_task(id):
    notification = Notification.objects.get(id=id)
    course = notification.course
    _, section, _ = course.retrieve_sections()
    first_name, email, topic, periodicTaskName = notification.get_periodic_task_attributes()

    questions_to_do = []
    _, current_questions = section.get_questions_for_student(notification.student)
    for q in current_questions:
        q_str = list(q.keys())[0]
        q_id = q[q_str]["question_id"]
        questions_to_do.append(f'{q_id} {q_str}')

    if len(questions_to_do) != 0:
        logger.info("Sent reminder email")
        return send_email(first_name, email, topic, questions_to_do)
    else:
        logger.info("There are no questions to do")