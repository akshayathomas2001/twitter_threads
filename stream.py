import requests
import os
import json
import time
from thread import get_thread
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error
import pandas as pd
load_dotenv()
def create_server_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

connection = create_server_connection("localhost", "root", pw)
def create_database(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Database created successfully")
    except Error as err:
        print(f"Error: '{err}'")

def auth():
    return os.getenv("BEARER_TOKEN")


def create_url(user_id,since_id):
    # Replace with user ID below
    if since_id is None:
        return "https://api.twitter.com/2/users/{}/mentions?max_results=5".format(user_id)
    return "https://api.twitter.com/2/users/{}/mentions?max_results=5&since_id={}".format(user_id, since_id)


def get_params():
    return {"tweet.fields": "created_at,conversation_id,in_reply_to_user_id", "expansions":"in_reply_to_user_id,author_id"}


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

def get_data(user_id, since_id):
    dict = []
    list1 = []
    bearer_token = auth()
    url = create_url(user_id, since_id)
    headers = create_headers(bearer_token)
    params = get_params()
    json_response = connect_to_endpoint(url, headers, params)
    print(json.dumps(json_response, indent=4, sort_keys=True))       
    result_count = json_response['meta']['result_count']
    # since_id  = json_response['meta']['newest_id']
    if result_count == 0:
        # time.sleep(60)
        # print("No results")
        return (since_id,dict)
    since_id  = json_response['meta']['newest_id']
    data = json_response['data']
    new_file = open("tweet_id.txt","r+")
    for line in new_file:
        list1.append(line.rstrip("\n"))
    #f1 = new_file.read()
    for tweet in data:
        check = tweet['id']
        print(str(check))
        if str(check) not in list1:
                new_file.write(tweet["id"]+"\n")
                if tweet.get('in_reply_to_user_id'):
                    dict.append({'id': tweet['author_id'], 'conversation_id': tweet['conversation_id'], 'in_reply_to_user_id': tweet['in_reply_to_user_id']})
    print(list1)
    new_file.close()
    return (since_id,dict)
