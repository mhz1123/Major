from django.shortcuts import  render, redirect
from .forms import NewUserForm
from django.contrib.auth import login
from django.contrib import messages 
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
import wolframalpha
client = wolframalpha.Client("R4U7JP-TEAKU27YYE")


# Create your views here.
def index(request):
    return render(request, "first/index.html")

def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("first:index")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm
	return render (request=request, template_name="first/register.html", context={"register_form":form})


def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("first:index")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="first/login.html", context={"login_form":form})

def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("first:index")

def search(request):
	if request.method == "GET":
		search = request.GET.get('search')

	#res = client.query(search)
	# res1=next(res.results).text
	return render(request, "first/search_result.html",{
		"search":search
	})