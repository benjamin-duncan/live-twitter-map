import datetime

from django.urls import reverse
from rest_framework.test import APITestCase

from .. import views
from ..models import Tweet


class TestViews(APITestCase):
    @classmethod
    def setUpTestData(cls):
        Tweet.objects.create(
            text="tweet text",
            tweet_id="1234545234253",
            lat=1.5,
            lon=50,
            timestamp_ms=round(datetime.datetime.now().timestamp() * 1000),
        )

    # /api/health/
    def test_health(self):
        url = reverse("health")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    # /api/stats/
    def test_stats(self):
        url = reverse("stats")
        response = self.client.get(url)

        self.assertEqual(response.data, {"total": 1, "day": 1, "hour": 1, "minute": 1})

    # startup
    def test_startup(self):
        url = reverse("startup")
        response = self.client.get(url)
        data = Tweet.objects.get(id=1)

        self.assertEqual(
            response.data,
            [
                {
                    "id": data.id,
                    "text": data.text,
                    "tweet_id": data.tweet_id,
                    "lat": data.lat,
                    "lon": data.lon,
                    # timestamp_ms as str to prevent JavaScript concatenating ints
                    "timestamp_ms": str(data.timestamp_ms),
                }
            ],
        )

    # graph
    def test_graph(self):
        url = reverse("graph")
        response = self.client.get(url)

        self.assertEqual(response.data[0]["y"], 1)

    # trailing slash - e.g. redirect /health to /health/
    def test_slash(self):
        response = self.client.get("/health")

        self.assertEqual(response.status_code, 301)
