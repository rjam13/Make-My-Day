from django_celery_beat.models import CrontabSchedule, PeriodicTask
import json
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from random import randint


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=255, default="", unique=True)
    student_id = models.CharField(max_length=255, blank=True)
    instructor_id = models.CharField(max_length=255, blank=True)

    def save(self, *args, **kwargs):
        if self._state.adding:
            super(UserProfile, self).save(*args, **kwargs)
            if self.instructor_id:
                instructor = Instructor()
                instructor.user_profile = self
                instructor.instructor_id = self.instructor_id
                instructor.save()
            if self.student_id:
                student = Student()
                student.user_profile = self
                student.student_id = self.student_id
                student.save()
        else:
            super(UserProfile, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.user.username)


class Instructor(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    instructor_id = models.CharField(max_length=255, primary_key=True)

    def __str__(self):
        return str(self.instructor_id)

    def retrieve_courses(self):
        return self.course_set.order_by('name')


class Student(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=255, primary_key=True)

    def __str__(self):
        return str(self.student_id)

    def retrieve_courses(self):
        return self.course_set.order_by('name')

def current_year():
    return timezone.now().year

def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)

class Course(models.Model):
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student, through="Notification")

    course_id = models.BigAutoField(primary_key=True, db_column="course_id")
    name = models.CharField(max_length=255)
    description = models.TextField(default="")
    access_code = models.CharField(max_length=100, default="", blank=True)
    year = models.PositiveIntegerField(default=timezone.now().year, validators=[MinValueValidator(1900), max_value_current_year])
    SPRING = "SPRING"
    SUMMER = "SUMMER" # this means once every two days
    FALL = "FALL"
    CHOICES = (
        (SPRING, "Spring"),
        (SUMMER, "Summer"),
        (FALL, "Fall"),
    )
    semester = models.CharField(choices = CHOICES, default=SUMMER, max_length=120)

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        if self.access_code == "":
            self.access_code = self.generateCode()
            super(Course, self).save(*args, **kwargs)
        else:
            super(Course, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('course_update', kwargs={'course_id': self.course_id})    

    def retrieve_sections(self):
        closed_sections = self.section_set.filter(
            end_date__lte=timezone.now())
        # there should only be one open_section
        open_section = self.section_set.filter(
            start_date__lte=timezone.now(), 
            end_date__gte=timezone.now()).first()
        upcoming_sections = self.section_set.filter(
            start_date__gte=timezone.now())

        return [closed_sections, open_section, upcoming_sections]
    
    def generateCode(self):
        with open('main/resources/adjectives.txt', 'r') as a, open('main/resources/nouns.txt', 'r') as n:
            adjectives = a.readlines()
            nouns = n.readlines()
            code = adjectives[randint(0, len(adjectives)-1)].strip() + nouns[randint(0, len(nouns)-1)].strip() + str(randint(10, 100))
            return code

class Notification(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, default=None)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, default=None)
    schedule = models.OneToOneField(CrontabSchedule, on_delete=models.CASCADE, default=None, null=True)
    time_to_send = models.TimeField(null=True)

    def save(self, *args, **kwargs):
        if self._state.adding:
            # SET UP AUTOMATED SENDING OF EMAILS HERE
            # resource: https://django-celery-beat.readthedocs.io/en/latest/#:~:text=To%20create%20a%20periodic%20task,schedule%2C%20created%20%3D%20IntervalSchedule.
            first_name, email, course, periodic_task_name = self.get_periodic_task_attributes()
            self.schedule = CrontabSchedule.objects.create(
                minute=str(self.time_to_send)[3:5],
                hour=str(self.time_to_send)[0:2],
                day_of_week='*',
                day_of_month='*',
                month_of_year='*',
                timezone='US/Eastern'
            )
            super(Notification, self).save(*args, **kwargs)
            PeriodicTask.objects.create(
                crontab=self.schedule,
                name=periodic_task_name,
                task='send_email_task',
                args=json.dumps([self.id]),
            )
            print(self.id)
        else:
            super(Notification, self).save(*args, **kwargs)
    
    # This function does not run when deleting multiple aqbs
    def delete(self, *args, **kwargs):
        if self.schedule:
            self.schedule.delete()
        super(Notification, self).delete(*args, **kwargs)
    
    def get_periodic_task_attributes(self):
        first_name = str(self.student.user_profile.user.first_name)
        email = str(self.student.user_profile.user.email)
        course = str(self.course)
        periodic_task_name = f'{str(self.pk)} Email Reminder: {str(self.student)}, {course}'
        return first_name, email, course, periodic_task_name