from django.shortcuts import  render, redirect
from .forms import SignUpForm, LoginForm
from .models import UserOperations
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth import authenticate, logout

def sign_up_view(request):
	haveError = False
	form = None
	if request.method == "POST":
		form = SignUpForm(request.POST)
		if form.is_valid():
			user = form.save()
			form.sendLink(user)
			return redirect("enters:succesfull-signup")
		else:
			haveError = True
	if not haveError:
		form = SignUpForm()
		for field in form:
			print(field.help_text)
	else:
		if form is not None:
			for field in form:
				for error in field.errors:
					print(field.errors)
	print('======================')
	context = {"register_form" : form, "register_title": "Please sign up", "register_button": "Signup"}
	return render (request=request, template_name="enters/register.html", context=context)

def success_message_view(request):
	return render (request=request, template_name="enters/success_page.html")

def validate_user(request,uid):
	result = UserOperations.set_user_activation(uid);
	return render (request=request, template_name="enters/activation_result.html", context={"isActivated":result})

def login_view(request):
    haveError = False
    form = None
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.login(request)
            if user:
                if user.is_active: 
                    login(request, user)
                    request.session['user_id'] = user.id
                    redirect_url = UserOperations().create_personal_info(user)
                    return redirect(redirect_url)
                
                return render(request ,"enters/not_active.html")

    if not haveError:
        form = LoginForm()
    context = {"register_form" : form, "register_title": "Please login", "register_button": "Login"}
    return render (request=request, template_name="enters/register.html", context=context)


def post_first_login_view(request):
	return render (request=request, template_name="enters/first_entrance.html")

def logout_user(request):
    
    logout(request)
    request.session['user_id'] = -1
    return redirect("enters:login")
