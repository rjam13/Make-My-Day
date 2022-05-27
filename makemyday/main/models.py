from cgitb import text
from django.db import models

# Create your models here.
class Question(models.Model):
    # name = the sentence itself
    number = models.IntegerField(null=True)
    ques = models.CharField(max_length= 200)

    def __str__(self):
        return self.ques

class Answer(models.Model):
    # text = the answer itself
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    ans = models.CharField(max_length= 300)
    isCorrect = models.BooleanField()

    def __str__(self):
        return self.ans