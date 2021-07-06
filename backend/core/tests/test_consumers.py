import asyncio

import pytest
from channels.testing import WebsocketCommunicator
from channels.layers import get_channel_layer

from core.consumers import TweetsConsumer


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_consumer_connection():
    communicator = WebsocketCommunicator(TweetsConsumer, "/ws/tweets/")

    connected, subprotocol = await communicator.connect()

    assert connected
    assert subprotocol is None

    await communicator.disconnect()


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_channels_layer_and_send():
    communicator = WebsocketCommunicator(TweetsConsumer, "/ws/tweets/")

    connected, subprotocol = await communicator.connect()

    layer = get_channel_layer()
    await layer.group_send(
        TweetsConsumer.GROUP, {"type": "text_message", "message": "hello"}
    )

    message = await communicator.receive_from()

    assert message == '{"message": "hello"}'

    await communicator.disconnect()
