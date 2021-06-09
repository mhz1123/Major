from django.shortcuts import  render, redirect
from .forms import NewUserForm
from django.contrib.auth import login
from django.contrib import messages 
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
import wolframalpha
import wikipedia
import re
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup

client = wolframalpha.Client("R4U7JP-TEAKU27YYE")



# Create your views here.
def index(request):

	url = 'https://www.sciencedaily.com/news/matter_energy/physics/'

	req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})

	webpage = urlopen(req).read()

	page_soup = soup(webpage, "html.parser")

	containers = page_soup.findAll("h3")

	

	head_list = []
	data_list = []
	# link_list = []
	for container in containers:
		head_list.append(container.text)


	summary =page_soup.find_all("div", {"class": "latest-summary"})

	for data in summary:
		data_list.append(data.text)

	len_head_list = len(head_list)-1

	# links=page_soup.find_all("h3.a")
	# for link in links:
	# 	link_list.append(link.text)

	scraped_res = {}
	for key in head_list:
		for value in data_list:
			scraped_res[key] = value
			data_list.remove(value)
			break  
	
		
	return render(request, "first/index.html",{
		"head_list":head_list,
		"scraped_res":scraped_res,
		"data_list":data_list,
		"len_head_list":len_head_list,
		# "link_list":link_list,
	})

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
		
	# search_str=""
	res = client.query(search)
	res1=next(res.results).text
	wiksearch=wikipedia.summary(search, sentences=10)

	return render(request, "first/search_result.html",{
		"search":search,
		"res1":res1,
		"wiksearch":wiksearch,
		
	})