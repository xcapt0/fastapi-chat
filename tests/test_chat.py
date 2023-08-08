import pytest
from fastapi import WebSocketDisconnect

from tests.conftest import client


def test_chat_unauthorized():
    with pytest.raises(WebSocketDisconnect):
        with client.websocket_connect("/chat/ws"):
            pass


async def test_chat_connection(ws_client):
    response = ws_client.receive_json()
    assert response["data"]["author"] == "System"
    assert response["data"]["text"] == "Test connected to the chat"


async def test_send_message(ws_client):
    ws_client.send_text("Hello world!")
    response = ws_client.receive_json()
    assert response["data"]["author"] == "Test"
    assert response["data"]["text"] == "Hello world!"
