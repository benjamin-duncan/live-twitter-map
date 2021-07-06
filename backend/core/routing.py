from django.urls import re_path

from .consumers import TweetsConsumer

websocket_urlpatterns = [
    re_path(r"ws/tweets/$", TweetsConsumer),
]
