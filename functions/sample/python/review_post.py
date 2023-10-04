"""IBM Cloud Function that gets all reviews for a dealership

Returns:
    List: List of reviews for the given dealership
"""
from cloudant.client import Cloudant
from cloudant.error import CloudantException
import requests


def main(param_dict):
    """Main Function

    Args:
        param_dict (Dict): input paramater

    Returns:
        _type_: _description_ TODO
    """

    try:
        client = Cloudant.iam(
            account_name=param_dict["COUCH_USERNAME"],
            api_key=param_dict["IAM_API_KEY"],
            connect=True,
        )

        rev=param_dict.get("review", None)
        if rev is None:
            return {"statusCode": 400, "body": "supply review object"}

        doc = {
            "id": rev["id"],
            "name": rev["name"],
            "dealership": rev["dealership"],
            "review": rev["review"],
            "purchase": rev["purchase"],
            "another": rev["another"],
            "purchase_date": rev["purchase_date"],
            "car_make": rev["car_make"],
            "car_model": rev["car_model"],
            "car_year": rev["car_year"]
        }

        my_database = client['reviews']
        ret = my_database.create_document(doc)
        if len(ret)==0:
            return {"statusCode":404, "body": "Unable to locate reviews for the dealer"}
        return {"reviews": ret}
    except CloudantException as cloudant_exception:
        print("unable to connect")
        return {"statusCode": 500, "body": cloudant_exception}
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"statusCode": 500, "body": err}
