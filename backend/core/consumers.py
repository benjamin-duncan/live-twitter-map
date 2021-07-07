import json
import os
import uuid
import random
import re

from channels.db import database_sync_to_async
from channels.generic.websocket import (
    AsyncWebsocketConsumer,
    AsyncJsonWebsocketConsumer,
)
from django.core.exceptions import ObjectDoesNotExist

from .redis import redis


class TweetsConsumer(AsyncWebsocketConsumer):
    GROUP = "tweet"
    flag = 1

    async def connect(self):

        self.flag = uuid.uuid4().hex
        redis.set(f"filter {self.flag}", "")
        if False:  # self.scope["user"].is_anonymous:
            await self.close()
        else:
            await self.channel_layer.group_add(self.GROUP, self.channel_name)
            await self.accept()

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        redis.set(f"filter {self.flag}", message)

        await self.channel_layer.group_send(
            self.GROUP, {"type": "text_message", "message": message}
        )

    async def text_message(self, event):
        if True:
            message = event["message"]

            filter = redis.get(f"filter {self.flag}")

            if filter in message:
                await self.send(text_data=json.dumps({"message": message}))


class GameConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()
        session = str(uuid.uuid4())
        redis.set(session, 0)
        await self.send_json({"session": session})
        await self.send_question()

    async def disconect(self):
        await self.disconnect()

    async def receive(self, text_data):
        response = json.loads(text_data)
        id = response.get("id", None)
        answer = response.get("answer", None)
        session = response.get("session", None)

        if id is None or answer is None or session is None:
            await self.send_json({"error": "invalid JSON"})

        elif redis.get(id) is None:
            await self.send_json({"error": "question already answered"})

        elif redis.get(id) == answer:
            score = int(redis.get(session)) + 1
            redis.set(session, score)
            await self.send_json({"response": "correct", "score": score})

        else:
            redis.set(session, 0)
            await self.send_json({"response": "incorrect", "score": 0})

        redis.delete(id)
        await self.send_question()

    async def send_question(self):
        question = str(uuid.uuid4())
        redis.set(question, "London")
        tweet = await self.get_random_tweet()
        # print(vars(tweet))
        try:
            if tweet.lon > 53:
                redis.set(question, "North")
            else:
                redis.set(question, "South")
            await self.send_json(
                {"question": question, "text": tweet.text, "lat": tweet.lon}
            )
        except AttributeError:
            await self.send_json({"error": "something didn't work :("})

    @database_sync_to_async
    def get_random_tweet(self):
        from .models import Tweet

        while True:
            try:
                query = Tweet.objects.get(id=random.randint(1, Tweet.objects.count()))
                query.text = re.sub("https?:\/\/(t\.co)?[^\s]*", "", query.text)
                if len(query.text) > 60 and query.lon is not None:
                    break
            except ObjectDoesNotExist:
                continue

        return query
