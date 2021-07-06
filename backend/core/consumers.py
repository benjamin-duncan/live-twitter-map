import json
import os
import uuid

from channels.generic.websocket import AsyncWebsocketConsumer

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
