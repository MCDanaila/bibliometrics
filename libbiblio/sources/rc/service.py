import os
import requests
from dotenv import load_dotenv

load_dotenv()
HEADERS = {'accept': '*/*', 'content-type': 'application/json'}
class RC_Api:
    def search(parameters):
        parameters.update({
            "apikey": os.environ.get("RC_API_KEY")
        })
        response = requests.get(os.environ.get("RC_API_SEARCH_URL"), params=parameters, headers=HEADERS)
        if response.status_code == 200:
            #print(f"service.py - INFO - sucessfully fetched records from search API !")
            return response.json()
        else:
            print(
                f"service.py - ERROR - There's a {response.status_code} error with your request !")
            return None


    def get_items(parameters):
        parameters.update({
            "apikey": os.environ.get("RC_API_KEY")
        })
        response = requests.get(os.environ.get("RC_API_ITEMS_URL"), params=parameters)
        if response.status_code == 200:
            #print(f"service.py - INFO - sucessfully fetched records from items API !")
            return response.json()
        else:
            print(
                f"service.py - ERROR - There's a {response.status_code} error with your request !")
            return None




