from __future__ import absolute_import, unicode_literals
import os
import time

from asgiref.sync import async_to_sync
from celery import Celery
import channels.layers
from django.core import serializers

from .consumers import TweetsConsumer
from .redis import redis


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
app = Celery("config")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(1, tweet_beat.s(), name="beat every 1 seconds")


@app.task
def tweet_beat(group=TweetsConsumer.GROUP, event="text_message"):
    from .models import Tweet

    t = int(time.time()) * 1000
    max_tweet = Tweet.objects.filter(timestamp_ms__lt=t).order_by("-timestamp_ms")[0]
    max_id = max_tweet.id

    if redis.get("id") is None:
        redis.set("id", max_id)

    id = int(redis.get("id"))

    if not id:
        id = max_id
    print(f"Pre loop id: {id}")
    messages = Tweet.objects.filter(id__range=[id, max_id])
    channel_layer = channels.layers.get_channel_layer()
    if messages and max_id is not redis.get("max_id_chk"):
        id = max_id + 1
        print(f"start loop id: {id}")
        redis.set("id", id)
        redis.set("max_id_chk", max_id)

        for message in messages:
            async_to_sync(channel_layer.group_send)(
                group,
                {
                    "type": event,
                    "message": serializers.serialize(
                        "json",
                        [
                            message,
                        ],
                    ),
                },
            )

    else:
        print(
            f"No Tweets in Range: {id} to {max_id}.\n Please Check if Database Stream is Live2"
        )

    print(f"final id: {id}")
    print(f"redis id: {redis.get('id')}")
