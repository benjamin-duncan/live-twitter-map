import datetime

from django.test import TestCase

from ..models import Tweet


class TestTweets(TestCase):
    def test_create_object(self):
        id = "1234545234253"
        Tweet.objects.create(
            text="tweet text",
            tweet_id="1234545234253",
            lat=1.5,
            lon=50,
            timestamp_ms=round(datetime.datetime.now().timestamp() * 1000),
        )

        self.assertEqual(Tweet.objects.count(), 1)

        query = Tweet.objects.filter(tweet_id="1234545234253")

        for tweet in query:
            self.assertEqual(tweet.text, "tweet text")
