from makemyday.celery import app
from celery.utils.log import get_task_logger
import questions.models as questions_model
from .email import send_email

logger = get_task_logger(__name__)

@app.task(name="send_email_task")
def send_email_task(id):
    aqb = questions_model.Activated_Question_Bank.objects.get(id=id)
    first_name, email, topic, periodicTaskName = aqb.get_periodic_task_attributes()

    # retrieves all the open questions that have not been answered
    questions_to_do = {}
    _, open_qs, _ = aqb.question_bank.get_questions_for_student(aqb.student)
    for q in open_qs:
        q_str = list(q.keys())[0]
        answerIsCorrect = q[q_str]["answerIsCorrect"]

        if answerIsCorrect is not "": # empty string == not answered
            q_id = q[q_str]["question_id"]
            q_closeDT = q[q_str]["closeDT"][0:16]
            q_time = q[q_str]["time_Limit"]
            q_weight = q[q_str]["weight"]
            questions_to_do[f'{q_id} {q_str}'] = f'Due: {q_closeDT} | Time: {q_time} minutes | {q_weight} pts'

    if len(questions_to_do) != 0:
        logger.info("Sent reminder email")
        return send_email(first_name, email, topic, questions_to_do)
    else:
        logger.info("There no questions to do")