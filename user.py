import os
import requests
import json
import time
from thread import get_thread
from dotenv import load_dotenv
load_dotenv()

def auth():
    return os.getenv("BEARER_TOKEN")


def create_url(user_id):
    return  "https://api.twitter.com/2/users/by/username/{}".format(user_id)


def get_params():
    return {}


def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


def connect_to_endpoint(url, headers, params):
    response = requests.request("GET", url, headers=headers, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()

def get_user_id(username):
    bearer_token = auth()
    headers = create_headers(bearer_token)
    params = get_params()
    url = create_url(username)
    json_response = connect_to_endpoint(url, headers, params)
    if json_response['data']:
        return json_response['data']['id']
