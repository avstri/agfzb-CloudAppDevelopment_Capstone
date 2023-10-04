from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarDealer, CarMake, CarModel
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create your views here.

# Create an `about` view to render a static about page
def about(request):
    context = {}
    # If the request method is GET
    if request.method == 'GET':
        return render(request, 'djangoapp/about.html', context)

# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    # If the request method is GET
    if request.method == 'GET':
        return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            print("user is not none")
            login(request, user)
            print("logged in")
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/user_login.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        passwordconfirm = request.POST['pswconfirm']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.debug("{} is new user".format(username))
        if not user_exist:
            if password != passwordconfirm:
                logger.warn("passwords don't match")
                context['message'] = "Passwords don't match"
                return render(request, 'djangoapp/registration.html', context)
            else:
                user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                                password=password)
                login(request, user)
                return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        url = "https://us-east.functions.appdomain.cloud/api/v1/web/683c092f-ee24-42f9-8048-b08ab7583220/dealership-package/get-dealership.json"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealer_names = '<br>'.join([f"{dealer.short_name} - {dealer.st}" for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(dealer_names)

def get_dealers_by_state(request):
    if request.method == "GET":
        url = "https://us-east.functions.appdomain.cloud/api/v1/web/683c092f-ee24-42f9-8048-b08ab7583220/dealership-package/get-dealership.json"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url, state=request.GET["state"])
        # Concat all dealer's short name
        dealer_names = '<br>'.join([f"{dealer.short_name} - {dealer.st}" for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(dealer_names)

# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        url = "https://us-east.functions.appdomain.cloud/api/v1/web/683c092f-ee24-42f9-8048-b08ab7583220/dealership-package/review.json"
        # Get dealers from the URL
        reviews = get_dealer_reviews_from_cf(url, dealerId=dealer_id)
        # Concat all dealer's short name
        dealer_names = ''.join([f"<p><b>{r.name} - {r.car_make} {r.car_model} {r.car_year}</b> <br>{r.review} <br>{r.sentiment}</p>" for r in reviews])
        # Return a list of dealer short name
        return HttpResponse(dealer_names)

# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    if not request.user.is_authenticated:
        redirect(login)
        return

    context = {"dealer_id": int(dealer_id)}
    if request.method == 'GET':
        return render(request, 'djangoapp/add_review.html', context)
    elif request.method == 'POST':
        url = "https://us-east.functions.appdomain.cloud/api/v1/web/683c092f-ee24-42f9-8048-b08ab7583220/dealership-package/reviewPost.json"
        review_text = request.POST['review']
        review = {}
        review["name"] = f"{request.user.first_name} {request.user.last_name}"
        review["dealership"] = int(dealer_id)
        review["review"] = review_text
        review["purchase"] = request.POST['purchase']
        review["car_make"] = request.POST['car_make']
        review["car_model"] = request.POST['car_model']
        review["car_year"] = request.POST['car_year']
        review["id"] = 1
        review["purchase_date"] = datetime.utcnow().isoformat()
        response = post_request(url,{"review":review})
        print(f"post review response {response}")
        return redirect("djangoapp:dealer_details",dealer_id = int(dealer_id))