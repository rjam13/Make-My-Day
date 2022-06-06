from cgitb import text
from django.db import models
# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
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

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=255, default = None)
    student_id = models.CharField(max_length=255, default=None)
    instructor_id = models.CharField(max_length=255, default=None)

    def __str__(self):
        return self.user.username

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         UserProfile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()


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