from cgitb import text
from tabnanny import verbose
from django.db import models
# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=255, default="", unique=True)
    student_id = models.CharField(max_length=255, default="")
    instructor_id = models.CharField(max_length=255, default="")

    def save(self, *args, **kwargs):
        print("foo")
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

class Student(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=255, primary_key=True)

class Course(models.Model):
    instructors = models.ManyToManyField(Instructor, related_name="instructors+")
    students = models.ManyToManyField(Student, related_name="students+")

    course_id = models.BigAutoField(primary_key=True, db_column="course_id")
    course_name = models.CharField(max_length=255)
    description = models.TextField(default="")

    def __str__(self):
        return str(self.course_name)

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
