from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from main.models import UserProfile
from register.form import RegisterForm, UserProfileForm



# def register(response):
#     # form = UserCreationForm()
#     # return render(response, "register/register.html", {"form": form})
# 	if response.method == 'POST':
# 		form = RegisterForm(response.POST)
# 		if form.is_valid():
# 			form.save(commit= False)

# 		return redirect("/home")	
# 	else:
# 		form = RegisterForm()
# 	return render(response, "register/register.html", {"form": form})


def register(request):
	if request.method == 'POST':
		instance_form = RegisterForm(request.POST)
		profile_form = UserProfileForm(request.POST)
		if instance_form.is_valid() and profile_form.is_valid():
			user = instance_form.save()

			profile = profile_form.save(commit= False)
			profile.user = user

			profile.save()

			username = instance_form.cleaned_data.get('username')
			print(username)
			password = instance_form.cleaned_data.get('password1')
			print(password)
			user = authenticate(username = username, password = password)
			login(request, user)

		return redirect("/home")	
	else:
		instance_form = RegisterForm()
		profile_form  = UserProfileForm()
	context = {'form': instance_form, 'profile_form': profile_form}	
	return render(request, "register/register.html", context)