from user import get_user_id
from stream import get_data
from thread import get_thread
import os
import time
from dm import send_threads


def main():
    username = "Threadifier"
    user_id = get_user_id(username)
    since_id = None
    while True:
        since_id, mentioned_tweets = get_data(user_id, since_id)
        print(mentioned_tweets)
        time.sleep(10)
        threads = get_thread(mentioned_tweets)
        print(threads)
        time.sleep(10)
        send_threads(threads)
        time.sleep(60)


if __name__ == '__main__':
    main()


