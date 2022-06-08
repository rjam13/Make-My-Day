from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm #add this
from main.models import UserProfile
from django.contrib import messages
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

def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			current_user = authenticate(username=username, password=password)
			if current_user is not None:
				login(request, current_user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("/home")
			else:
				messages.error(request,"Invalid username/password.")
		else:
			messages.error(request,"Invalid username/password.")
	form = AuthenticationForm()
	return render(request=request, template_name="register/login.html", context={"login_form":form})	