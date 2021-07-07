from django.urls import re_path

from .consumers import TweetsConsumer, GameConsumer

websocket_urlpatterns = [
    re_path(r"ws/tweets/$", TweetsConsumer),
    re_path(r"ws/game/$", GameConsumer)
]
