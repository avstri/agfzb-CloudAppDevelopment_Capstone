import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth

def get_request(url, **kwargs):
    print(kwargs)
    print(f"GET from {url} ")
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
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
    json_result = get_request(url, **kwargs)
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
    json_result = get_request(url, **kwargs)
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
                                   car_year=review["car_year"], id=review["id"])
            results.append(r_obj)

    return results
