import requests
import os
import json
import time
from dotenv import load_dotenv
load_dotenv()

def auth():
    return os.getenv("BEARER_TOKEN")


def create_url(ref_id, author_id,main_tweet = False):

    if main_tweet:
        return "https://api.twitter.com/2/tweets/{}".format(ref_id)
    return "https://api.twitter.com/2/tweets/search/recent?query=conversation_id:{}%20from%3A{}&max_results=50".format(ref_id, author_id)

def get_params():
    return {"tweet.fields": "created_at,conversation_id", "expansions":"in_reply_to_user_id,author_id"}


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


def get_thread(dict):
    threads = []
    for item in dict:
        thread = {}
        bearer_token = auth()
        headers = create_headers(bearer_token)
        params = get_params()
        conversation_id = item['conversation_id']
        in_reply_to_user_id = item['in_reply_to_user_id']
        thread['id'] = item['id']
        thread['text'] = ""

        main_tweet_url = create_url(conversation_id, in_reply_to_user_id, True)
        main_tweet_json_response = connect_to_endpoint(main_tweet_url, headers, params)
        main_tweet  = main_tweet_json_response['data']['text']
        thread['text'] = main_tweet + "\n"

        url = create_url(conversation_id, in_reply_to_user_id)
        json_response = connect_to_endpoint(url, headers, params)
        print(json.dumps(json_response, indent=4, sort_keys=True))
        result_count = json_response['meta']['result_count']
        if result_count > 0:
            text_list = []
            data = list(reversed(json_response['data']))
            for tweet in data:
                if tweet["author_id"] == tweet["in_reply_to_user_id"]:
                    text_list.append(tweet['text'])
            print(thread['text']+"\n".join(text_list))
            thread['text'] = thread['text'] + "\n".join(text_list)
        threads.append(thread)
    return threads

