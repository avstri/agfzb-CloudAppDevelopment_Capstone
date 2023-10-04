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

        dealer_id=param_dict.get("dealerId", None)
        my_database = client['reviews']
        if dealer_id is not None:
            ret = my_database.get_query_result({'dealership' : int(dealer_id)})[:]
            if len(ret)==0:
                return {"statusCode":404, "body": "Unable to locate reviews for the dealer"}
            return {"reviews": ret}

        rows = my_database.all_docs(include_docs=True, limit=100)["rows"]
        ret = [r["doc"] for r in rows]
        return {"reviews": ret}
    except CloudantException as cloudant_exception:
        print("unable to connect")
        return {"statusCode": 500, "error": cloudant_exception}
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"statusCode": 500, "error": err}
