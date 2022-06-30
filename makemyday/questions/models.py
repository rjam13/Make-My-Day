from django.db import models
from main.models import Course, Student
import random
from datetime import datetime
from django.utils import timezone

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
    score = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    time_to_send = models.TimeField(null=True)

    def __str__(self):
        return str(self.pk)

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