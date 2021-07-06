"""
Standalone module for consuming Twitter streaming API
"""
import os
import random
import time

import tweepy
import psycopg2


class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        if hasattr(status, "place") and hasattr(status.place, "bounding_box"):
            cursor = mydb.cursor()

            add_tweet = "INSERT INTO tweets (text,tweet_id,lon,lat,timestamp_ms) VALUES (%s,%s,%s,%s,%s)"
            text = remove_emoji(status.text)

            centre = centre_bb(status.place.bounding_box)

            dt = (text, status.id, centre[0], centre[1], status.timestamp_ms)

            cursor.execute(add_tweet, dt)
            mydb.commit()


def centre_bb(bb):  # Takes bounding box and calculates centre point
    c1, c2 = [bb.coordinates[0][i] for i in (0, 2)]
    # centre = [(c1[1] + c2[1] )/2,(c1[0] + c2[0] )/2]
    centre = [
        random.triangular(c1[1], c2[1]),
        random.triangular(c1[0], c2[0]),
    ]  # Randomises to minimise stacking
    return centre


def remove_emoji(text):  # Removes emoji from text for database compatability
    if text:
        return text.encode("ascii", "ignore").decode("ascii")
    else:
        return None


def _connect():
    db = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USERNAME"),
        password=os.getenv("DB_PASSWORD"),
        dbname=os.getenv("DB_NAME"),
    )
    return db


if __name__ == "__main__":
    while True:
        time.sleep(5)
        try:
            mydb = _connect()
        except:
            print("Database loading...")
        print(mydb)
        auth = tweepy.OAuthHandler(
            os.getenv("CONSUMER_KEY"), os.getenv("CONSUMER_SECRET")
        )
        auth.set_access_token(os.getenv("ACCESS_TOKEN"), os.getenv("ACCESS_SECRET"))
        api = tweepy.API(auth)
        region = [-7.0, 49.0, 2.0, 61.0]

        myStreamListener = MyStreamListener()
        myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
        myStream.filter(locations=region)
        mydb.close()
        print("db closed")
