from django.db import models
from main.models import Course, Student
from datetime import datetime

# Create your models here.
class Section(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, default=None)
    section_id = models.BigAutoField(primary_key=True, db_column="section_id")
    topic = models.CharField(max_length=255, default="Topic")
    # NOTE: sections within the same course do not have overlapping dates (not yet implemented)
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    DAILY = "DAILY"
    BIDIURNAL = "BIDIURNAL" # this means once every two days
    WEEKLY = "WEEKLY"
    FREQUENCY_CHOICES = (
        (DAILY, "Daily"),
        (BIDIURNAL, "Every other day"),
        (WEEKLY, "Weekly"),
    )
    frequency = models.CharField(choices = FREQUENCY_CHOICES, default=DAILY, max_length=120) # not yet implemented

    def __str__(self):
        return str(self.topic)

    def get_questions(self):
        questions = list(self.question_set.all())
        return questions
    
    def get_questions_for_student(self, student):
        questions = list(self.question_set.all())
        past_questions = []
        current_questions = []
        future_questions = []

        for q in questions:
            question_Info = {}
            question_Info['open_datetime'] = str(q.open_datetime)
            question_Info['question_id'] = str(q.question_id)

            if student:
                # checks whether if the student has answered this question before or not
                responseToQuestion = Response.objects.filter(question=q, student=student).first()
                # has response has an answer (wrong or correct)
                if responseToQuestion and responseToQuestion.answer:
                    answer = Answer.objects.get(answer_id=responseToQuestion.answer.answer_id)
                    question_Info['answerIsCorrect'] = str(answer.is_correct)
                # has response but no answer (response was left blank)
                elif responseToQuestion:
                    question_Info['answerIsCorrect'] = "False"
                # no response
                else:
                    question_Info['answerIsCorrect'] = ""
            else:
                question_Info['answerIsCorrect'] = ""
            
            if q.open_datetime.date() == datetime.today().date():
                current_questions.append({str(q): question_Info})
            elif q.open_datetime.date() < datetime.today().date():
                past_questions.append({str(q): question_Info})
            else:
                future_questions.append({str(q): question_Info})

        return past_questions, current_questions

# This model is not really necessary, but is only kept for the sake of the statistics page
# should really be deleted since score can be calculated based on the students' responses
# class SectionScore(models.Model):
#     student = models.ForeignKey(Student, on_delete=models.CASCADE, default=None)
#     section = models.ForeignKey(Section, on_delete=models.CASCADE, default=None)
#     score = models.DecimalField(max_digits=6, decimal_places=2, null=True)

#     def __str__(self):
#         return str(self.pk)

#     def compute_score(self):
#         responses = Response.objects.filter(student=self.student, question__in=self.section.question_set.all())
#         # numberOfResponses is the total number of questions the student answered or Did not answer. 
#         # NOTE: This does not equal to the number of questions in a question bank
#         number_of_responses = len(responses)
#         number_of_correct = 0
#         for res in responses:
#             correctAns = res.question.answer_set.get(is_correct=True)
#             if res.answer == correctAns:
#                 number_of_correct += 1
        
#         if number_of_correct == 0:
#             self.score = 0
#         else:
#             self.score = number_of_correct/number_of_responses * 100
#         self.save()

class Question(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, default=None)
    question_id = models.BigAutoField(primary_key=True, db_column="question_id")
    text = models.TextField(default="")
    order = models.IntegerField(default=0)
    open_datetime = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"{str(self.text)}"

    def get_answers(self):
       return self.answer_set.all()

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, default=None)
    answer_id = models.BigAutoField(primary_key=True, db_column="answer_id")
    text = models.TextField(default="")
    is_correct = models.BooleanField(default=False)
    explanation = models.TextField(default="")

    def __str__(self):
        return f"question: {self.question.text}, answer: {self.text}, correct: {self.is_correct}"

class Response(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, default=None)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, blank=True, null=True, default=None)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, default=None)