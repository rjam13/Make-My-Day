from cgitb import text
from tabnanny import verbose
from django.db import models
# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=255, default="", unique=True)
    student_id = models.CharField(max_length=255, default="")
    instructor_id = models.CharField(max_length=255, default="")

    def save(self, *args, **kwargs):
        super(UserProfile, self).save(*args, **kwargs)
        if self._state.adding:
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

    def __str__(self):
        return self.user.username

class Instructor(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    instructor_id = models.CharField(max_length=255, primary_key=True)

class Student(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=255, primary_key=True)

class Course(models.Model):
    instructors = models.ManyToManyField(Instructor, related_name="instructors+")
    students = models.ManyToManyField(Student, related_name="students+")

    course_id = models.BigAutoField(primary_key=True, default=0, db_column="course_id")
    course_name = models.CharField(max_length=255)
    description = models.TextField(default="")

    def __str__(self):
        return self.course_name

class Question_Bank(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, default=None)
    assigned_students = models.ManyToManyField(Student, through="Activated_Question_Bank")
    question_bank_id = models.BigAutoField(primary_key=True, default=0, db_column="question_bank_id")
    
    topic = models.CharField(max_length=255, default="Topic")
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    number_of_attempts = models.IntegerField(default=3)
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

    def __str__(self):
        return self.topic

class Activated_Question_Bank(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, default=None)
    question_bank = models.ForeignKey(Question_Bank, on_delete=models.CASCADE, default=None)
    score = models.DecimalField(max_digits=3, decimal_places=2, null=True)
    time_to_send = models.TimeField(null=True)

class Question(models.Model):
    question_bank = models.ForeignKey(Question_Bank, on_delete=models.CASCADE, default=None)

    question_id = models.BigAutoField(primary_key=True, default=0, db_column="question_id")
    ques = models.TextField(default="")
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.ques

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, default=None)

    answer_id = models.BigAutoField(primary_key=True, default=0, db_column="answer_id")
    ans = models.TextField(default="")
    isCorrect = models.BooleanField(default=False)
    explanation = models.TextField(default="")

    def __str__(self):
        return self.ans

class Response(models.Model):
    ques = models.ForeignKey(Question, on_delete=models.CASCADE, default=None)
    ans = models.ForeignKey(Answer, on_delete=models.CASCADE, default=None)
    std = models.ForeignKey(Student, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.std_id + self.ques_id + self.ans_id

# class MyAccountManager(BaseUserManager): 
#     def create_user(self, username, password= None):
#         if not username:
#             raise ValueError("User must have an username")

#         user = self.model(
#             username=username,
#             )
#         user.set_password(password)
#         user.save(user = self._db)
#         return user  

#     def create_superuser(self, username, password):
#         user = self.create_user(
#              username=username,
#              password=password,
#             )
#         user.is_admin = True
#         user.is_staff = True
#         user.is_superuser = True
#         user.save(using = self._db)
#         return user



# class User(AbstractBaseUser, PermissionsMixin):
#     username = models.CharField(max_length = 30, unique = True)
#     email = models.EmailField(verbose_name="email", max_length=60, unique=True)
#     date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
#     last_login = models.DateTimeField(verbose_name= 'last login', auto_now =True)
#     is_admin = models.BooleanField(default=False)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#     is_superuser= models.BooleanField(default=False)

#     USERNAME_FIELD = 'username'
#     REQUIRED_FIELDS = []

#     objects = MyAccountManager()

#     def __str__(self):
#         return self.username

#     def has_perm(self, perm, obj = None):
#         return self.is_admin

#     def has_module_perms(self, app_label):
#         return True   

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         UserProfile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()
