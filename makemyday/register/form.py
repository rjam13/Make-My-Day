from stat import ST_UID
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
# from main.models import User
from django.contrib.auth.models import User
from main.models import UserProfile


class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)

        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]

        if commit:
            user.save()
        return user


class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ('phone', 'student_id', 'instructor_id')
