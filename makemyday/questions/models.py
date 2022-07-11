from django.db import models
from main.models import Course, Student
import random
from datetime import datetime
from django.utils import timezone
from emailtask.tasks import send_email_task
from django_celery_beat.models import CrontabSchedule, PeriodicTask
import json
import pytz


# Create your models here.

class Question_Bank(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, default=None)
    assigned_students = models.ManyToManyField(Student, through="Activated_Question_Bank")
    question_bank_id = models.BigAutoField(primary_key=True, db_column="question_bank_id")
    
    topic = models.CharField(max_length=255, default="Topic")
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    number_of_attempts = models.IntegerField(default=3) # might move to question model
    isRandom = models.BooleanField(default=False)
    DAILY = "DAILY"
    BIDIURNAL = "BIDIURNAL" # this means once every two days
    WEEKLY = "WEEKLY"
    FREQUENCY_CHOICES = (
        (DAILY, "Daily"),
        (BIDIURNAL, "Every other day"),
        (WEEKLY, "Weekly"),
    )
    frequency = models.CharField(choices = FREQUENCY_CHOICES, default=DAILY, max_length=120)

    class Meta:
        verbose_name_plural = 'Question_Banks'

    def __str__(self):
        return str(self.topic)

    def get_questions(self):
        questions = list(self.question_set.all())
        if self.isRandom:
            random.shuffle(questions)
        return questions

class Activated_Question_Bank(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, default=None)
    question_bank = models.ForeignKey(Question_Bank, on_delete=models.CASCADE, default=None)
    schedule = models.OneToOneField(CrontabSchedule, on_delete=models.CASCADE, default=None, null=True)
    time_to_send = models.TimeField(null=True)
    score = models.DecimalField(max_digits=6, decimal_places=2, null=True)

    def save(self, *args, **kwargs):
        if self._state.adding:
            # SET UP AUTOMATED SENDING OF EMAILS HERE
            # resource: https://django-celery-beat.readthedocs.io/en/latest/#:~:text=To%20create%20a%20periodic%20task,schedule%2C%20created%20%3D%20IntervalSchedule.
            first_name, email, topic, periodicTaskName = self.get_periodic_task_attributes()
            self.schedule = CrontabSchedule.objects.create(
                minute=str(self.time_to_send)[3:5],
                hour=str(self.time_to_send)[0:2],
                day_of_week='*',
                day_of_month='*',
                month_of_year='*',
                timezone='US/Eastern'
            )
            PeriodicTask.objects.create(
                crontab=self.schedule,
                name=periodicTaskName,
                task='send_email_task',
                args=json.dumps([first_name, email, topic]), # args: first_name, email, topic
            )
            super(Activated_Question_Bank, self).save(*args, **kwargs)
        else:
            super(Activated_Question_Bank, self).save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        self.schedule.delete()
        super(Activated_Question_Bank, self).delete(*args, **kwargs)

    def __str__(self):
        return str(self.pk)
    
    def get_periodic_task_attributes(self):
        first_name = str(self.student.user_profile.user.first_name)
        email = str(self.student.user_profile.user.email)
        topic = str(self.question_bank)
        periodicTaskName = f'{str(self.pk)} Email Reminder: {str(self.student)}, {topic}'
        return first_name, email, topic, periodicTaskName

    def computeScore(self):
        closed_qs = self.question_bank.question_set.filter(closeDT__lte=timezone.now())
        for q in closed_qs:
            # if this closed question does not have a response, create one that is not answered
            if not Response.objects.filter(std=self.student, ques=q):
                Response.objects.create(std=self.student, ques=q, ans=None)

        responses = Response.objects.filter(std=self.student, ques__in=self.question_bank.question_set.all())
        # numberOfResponses is the total number of questions the student answered or Did not answer. 
        # i.e. the number of questions with a green or red cover in the question bank page
        # NOTE: This does not equal to the number of questions in a question bank
        numberOfResponses = len(responses)
        numberOfCorrect = 0
        for res in responses:
            correctAns = res.ques.answer_set.get(isCorrect=True)
            if res.ans == correctAns:
                numberOfCorrect += 1
        
        if numberOfCorrect == 0:
            self.score = 0
        else:
            self.score = numberOfCorrect/numberOfResponses * 100
    
    def sendEmail(self):
        email = self.student.user_profile.user.email
        first_name = self.student.user_profile.user.first_name
        topic = str(self.question_bank)
        send_email_task.apply_async((first_name, email, topic), countdown=5)

class Question(models.Model):
    question_bank = models.ForeignKey(Question_Bank, on_delete=models.CASCADE, default=None)

    question_id = models.BigAutoField(primary_key=True, db_column="question_id")
    ques = models.TextField(default="")
    order = models.IntegerField(default=0)
    time_Limit = models.IntegerField(default=60, help_text="duration of the question in minutes")
    openDT = models.DateTimeField(default=datetime.now)
    closeDT = models.DateTimeField(default=datetime.now)
    weight = models.IntegerField(default=1)

    def __str__(self):
        # return str(self.ques)
        return f"{str(self.ques)}"

    def get_answers(self):
       return self.answer_set.all()

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, default=None)

    answer_id = models.BigAutoField(primary_key=True, db_column="answer_id")
    ans = models.TextField(default="")
    isCorrect = models.BooleanField(default=False)
    explanation = models.TextField(default="")

    def __str__(self):
        return f"question: {self.question.ques}, answer: {self.ans}, correct: {self.isCorrect}"

class Response(models.Model):
    ques = models.ForeignKey(Question, on_delete=models.CASCADE, default=None)
    ans = models.ForeignKey(Answer, on_delete=models.CASCADE, blank=True, null=True, default=None)
    std = models.ForeignKey(Student, on_delete=models.CASCADE, default=None)