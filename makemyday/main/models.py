from cgitb import text
from email.policy import default
from fileinput import close
from tabnanny import verbose
from django.db import models
# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator


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


#Possibly create some foreign keys for student and instructor
class Instructor(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    instructor_id = models.CharField(max_length=255, primary_key=True)

    def __str__(self):
        return str(self.instructor_id)


class Student(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=255, primary_key=True)

    def __str__(self):
        return str(self.student_id)

    def retrieveActivatedQuestionBanks(self):
        activated_qbs = self.activated_question_bank_set.all()
        closed_aqbs = []
        open_aqbs = []
        upcoming_aqbs = []
        for qb in activated_qbs:
            if qb.question_bank.end_date <= timezone.now():
                closed_aqbs.append(qb)
            elif qb.question_bank.start_date <= timezone.now() and qb.question_bank.end_date >= timezone.now():
                open_aqbs.append(qb)
            elif qb.question_bank.start_date >= timezone.now():
                upcoming_aqbs.append(qb)

        return [closed_aqbs, open_aqbs, upcoming_aqbs]

def current_year():
    return timezone.now().year

def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)

class Course(models.Model):
    instructors = models.ManyToManyField(Instructor, related_name="instructors")
    students = models.ManyToManyField(Student, related_name="students")

    course_id = models.BigAutoField(primary_key=True, db_column="course_id")
    course_name = models.CharField(max_length=255)
    description = models.TextField(default="")
    access_code = models.CharField(max_length=100, default="")
    year = models.PositiveIntegerField(default=timezone.now().year, validators=[MinValueValidator(1900), max_value_current_year])
    SPRING = "SPRING"
    SUMMER = "SUMMER" # this means once every two days
    FALL = "FALL"
    CHOICES = (
        (SPRING, "Spring"),
        (SUMMER, "Summer"),
        (FALL, "Fall"),
    )
    semester = models.CharField(choices = CHOICES, default=FALL, max_length=120)

    def __str__(self):
        return str(self.course_name)

    def get_absolute_url(self):
        return reverse('course_update', kwargs={'course_id': self.course_id})    

    # This retrieves question banks that are not closed (now is before question_bank.end_date)
    def retrieveQuestionBanks(self):
        closed_qbs = self.question_bank_set.filter(
            end_date__lte=timezone.now())
        open_qbs = self.question_bank_set.filter(
            start_date__lte=timezone.now(), 
            end_date__gte=timezone.now())
        upcoming_qbs = self.question_bank_set.filter(
            start_date__gte=timezone.now())

        return [closed_qbs, open_qbs, upcoming_qbs]



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
