import requests
import json
from os import getenv
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth

def get_request(url, api_key, **kwargs):
    print(f"GET from {url} ")
    try:
        # Call get method of requests library with URL and parameters
        if api_key:
            response = requests.get(url, params=kwargs, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey', api_key))
        else:
            response = requests.get(url, params=kwargs, headers={'Content-Type': 'application/json'})
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print(f"With status {status_code} ")
    json_data = json.loads(response.text)
    return json_data

def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, api_key=None, **kwargs)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["dealerships"]
        # For each dealer object
        for dealer in dealers:
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], 
                                   full_name=dealer["full_name"],
                                   id=dealer["id"], lat=dealer["lat"], 
                                   long=dealer["long"],
                                   short_name=dealer["short_name"],
                                   st=dealer["st"], zip=dealer["zip"])
            results.append(dealer_obj)

    return results

def get_dealer_reviews_from_cf(url, **kwargs):
    json_result = get_request(url, api_key=None, **kwargs)
    results = []
    if json_result:
        # Get the row list in JSON as dealers
        reviews = json_result["reviews"]
        # For each dealer object
        for review in reviews:
            # Create a DealerReview object with values in `doc` object
            r_obj = DealerReview(dealership=review["dealership"], name=review["name"],
                                   purchase=review["purchase"],
                                   review=review["review"], purchase_date=review["purchase_date"],
                                   car_make=review["car_make"],
                                   car_model=review["car_model"],
                                   car_year=review["car_year"],
                                   id=review["id"])
            r_obj.sentiment = analyze_review_sentiments(r_obj.review)
            results.append(r_obj)

    return results

def analyze_review_sentiments(dealerreview):
    params = dict()
    url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/703b9877-bedf-4c8c-a78e-a4ad490e5545/v1/analyze"
    api_key = getenv('NLU_API_KEY')
    params["text"] = dealerreview
    params["version"] = "2022-04-07"
    params["features"] = {"sentiment":{}}
    params["language"] = "en"
    # params["return_analyzed_text"] = dealerreview.review
    response = get_request(url, api_key, **params)
    if "sentiment" in response:
        return response['sentiment']['document']['label']
    return ""

def post_request(url, json_payload, **kwargs):
    try:
        # Call get method of requests library with URL and parameters
        response = requests.post(url, params=kwargs, headers={'Content-Type': 'application/json'},
            json=json_payload)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print(f"With status {status_code} {response.text}")
    json_data = json.loads(response.text)
    print(f"json {json_data}")
    return json_data
