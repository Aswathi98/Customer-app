from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Customer
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout , authenticate
from django.contrib import messages
from .forms import NewUserForm
from django.utils import timezone
import urllib.request

# Create your views here.

import bs4 as bs
import urllib.request
import re 
import tweepy 
from tweepy import OAuthHandler 
from textblob import TextBlob 
def scrapper(urlstring):
    source = urllib.request.urlopen(urlstring).read()
    soup = bs.BeautifulSoup(source,'lxml')
    for paragraph in soup.find_all('p'):
        block = str(paragraph.text)
        if block == None:
            pass
        else:
            print(str(paragraph.text))


def homepage(request):
    return render(request = request,template_name='main/home.html',
    context = {"customer": Customer.objects.all})

# def details(request,id):
#     return render(request = request,template_name='main/details.html',context = {"tut":Tutorial.objects.get(id=id)} )


def details(request,id):
    cust = Customer.objects.get(id=id)
    scrap_url = cust.customer_link
    if cust.customer_content == "":
        source = urllib.request.urlopen(scrap_url).read()
        soup = bs.BeautifulSoup(source,'lxml')
        txt = ""
        for paragraph in soup.find_all('p'):
            block = str(paragraph.text)
            if block == None:
                pass
            else:
                txt += (str(paragraph.text))

        cust.customer_content = txt
        cust.save()


    return render(request = request,template_name='main/details.html',
    context = {"cust":Customer.objects.get(id=id)} )




def register(request , backend='django.contrib.auth.backends.ModelBackend'):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"New account created: {username}")
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.info(request, f"you are now logged in as {username}")            
            return redirect("main:homepage")

        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")

            return render(request = request,
                          template_name = "main/register.html",
                          context={"form":form})

    form = NewUserForm
    return render(request = request,
                  template_name = "main/register.html",
                  context={"form":form})


def logout_request(request):    
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("main:homepage")

def interact(request):
  return render(request = request,
                  template_name = "main/chat.html",
                )


def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect('/')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")

    form = AuthenticationForm()
    return render(request = request,
                  template_name = "main/login.html",
                  context={"form":form})

def analytics(request):
    custs =  Customer.objects.all()

    
    consumer_key = 'TJEXk32gRn8wNgC32YhvX01mH'
    consumer_secret ='bRy1uq6pqIPD7xJ2id3lj4RJY0YgYZNdcMWYhZejErfQp2OybK'
    access_token = '1253570225141760000-d0dOtwUymDTbX1LAQKQcAkhyohC6wg'
    access_token_secret ='f8ju1in44dPMx78LO3NMzaATZKvqKlqdKlmFr9QqTMcRf'

    auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
    auth.set_access_token(access_token,access_token_secret)

    api= tweepy.API(auth)
    for names in custs:
         polarity = 0
         subjectivity =0
         customer_name = str(names.customer_name)
         public_tweets = api.search(customer_name)
         print(customer_name)

         for tweet in public_tweets:
             analysis=TextBlob(tweet.text)
             Sentiment= analysis.sentiment
             polarity += Sentiment.polarity
             subjectivity += Sentiment.subjectivity
             names.pol=polarity
             names.sub=subjectivity
             names.save()

    return render(request,template_name="main/analytics.html",context={'custs':custs})

