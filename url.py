import os
import requests
import json
from dotenv import load_dotenv
load_dotenv()

def auth():
    return os.getenv("BEARER_TOKEN")

def get_params(type):
    params = {
        "user": {},
        "threads": {"tweet.fields": "created_at,conversation_id", "expansions":"in_reply_to_user_id,author_id"},
        "stream": {"tweet.fields": "created_at,conversation_id,in_reply_to_user_id", "expansions":"in_reply_to_user_id,author_id"}
    }

    return params.get(type, {})

def create_url(type, ref_id, author_id):
    urls = {
        
    }
    return "https://api.twitter.com/2/tweets/search/recent?query=conversation_id:{}%20from%3A{}".format(ref_id, author_id)

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
