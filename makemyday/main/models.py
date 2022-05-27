from cgitb import text
from django.db import models

# Create your models here.
class Question(models.Model):
    # name = the sentence itself
    number = models.IntegerField(null=True)
    ques = models.CharField(max_length= 200)

    def __str__(self):
        return self.name

class Answer(models.Model):
    # text = the answer itself
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length= 300)
    isCorrect = models.BooleanField()

    def __str__(self):
        return self.text