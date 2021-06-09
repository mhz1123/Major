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
	link_list = []
	for container in containers:
		head_list.append(container.text)


	summary =page_soup.find_all("div", {"class": "latest-summary"})

	for data in summary:
		data_list.append(data.text)

	len_head_list = len(head_list)-1

	links=page_soup.find_all("h3",{"class": "latest-head"})
	
	for link in links:
		link_list.append(f"https://www.sciencedaily.com{link.a['href']}")

	scraped_res = {}
	for key in head_list:
		for value in data_list:
			scraped_res[key] = value
			data_list.remove(value)
			break  

	for data in summary:
		data_list.append(data.text)
	
	head_list1=head_list[1]
	head_list2=head_list[2]
	head_list3=head_list[3]
	head_list4=head_list[4]
	head_list5=head_list[5]
	head_list6=head_list[6]
	head_list7=head_list[7]
	head_list8=head_list[8]
	head_list9=head_list[9]
	head_list10=head_list[10]
	head_list11=head_list[11]
	head_list12=head_list[12]
	data_list1=data_list[1]
	data_list2=data_list[2]
	data_list3=data_list[3]
	data_list4=data_list[4]
	data_list5=data_list[5]
	data_list6=data_list[6]
	data_list7=data_list[7]
	data_list8=data_list[8]
	data_list9=data_list[9]
	data_list10=data_list[10]
	data_list11=data_list[11]
	data_list12=data_list[12]

	link_list1=link_list[1]
	link_list2=link_list[2]
	link_list3=link_list[3]
	link_list4=link_list[4]
	link_list5=link_list[5]
	link_list6=link_list[6]
	link_list7=link_list[7]
	link_list8=link_list[8]
	link_list9=link_list[9]
	link_list10=link_list[10]
	link_list11=link_list[11]
	link_list12=link_list[12]

		
	return render(request, "first/index.html",{
		"head_list":head_list,
		"scraped_res":scraped_res,
		"data_list":data_list,
		"len_head_list":len_head_list,

		"head_list1":head_list1,
		"head_list2":head_list2,
		"head_list3":head_list3,
		"head_list4":head_list4,
		"head_list5":head_list5,
		"head_list6":head_list6,
		"head_list7":head_list7,
		"head_list8":head_list8,
		"head_list9":head_list9,
		"head_list10":head_list10,
		"head_list11":head_list11,
		"head_list12":head_list12,

		"data_list1":data_list1,
		"data_list2":data_list2,
		"data_list3":data_list3,
		"data_list4":data_list4,
		"data_list5":data_list5,
		"data_list6":data_list6,
		"data_list7":data_list7,
		"data_list8":data_list8,
		"data_list9":data_list9,
		"data_list10":data_list10,
		"data_list11":data_list11,
		"data_list12":data_list12,

		"link_list1":link_list1,
		"link_list2":link_list2,
		"link_list3":link_list3,
		"link_list4":link_list4,
		"link_list5":link_list5,
		"link_list6":link_list6,
		"link_list7":link_list7,
		"link_list8":link_list8,
		"link_list9":link_list9,
		"link_list10":link_list10,
		"link_list11":link_list11,
		"link_list12":link_list12,

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