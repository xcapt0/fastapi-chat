import json
import uuid
from typing import Dict

import aioredis
from starlette.websockets import WebSocket

from .schema import ChatDataSchema, ChatSchema
from .utils import generate_color
from config import REDIS_HOST


class MessageHistoryManager:
    def __init__(self):
        self.redis = aioredis.from_url(REDIS_HOST, decode_responses=True)

    async def add(self, unique_id: str, user: dict, message: str):
        user["message"] = message
        await self.redis.rpush(unique_id, json.dumps(user))

    async def get_list(self, unique_id: str):
        messages = await self.redis.lrange(unique_id, 0, -1)
        return [json.loads(message) for message in messages]


class WebSocketManager:
    def __init__(self):
        self.connected_clients: Dict[WebSocket, dict] = {}
        self.system_user = {"username": "System", "color": "red"}
        self.history = MessageHistoryManager()
        self.unique_id = uuid.uuid4().hex

    async def connect(self, websocket: WebSocket, user: dict):
        await websocket.accept()

        user['color'] = generate_color()
        self.connected_clients[websocket] = user

        await self.load_history(websocket)
        await self.broadcast(message=f"{user['username']} connected to the chat", user=self.system_user)

    async def disconnect(self, websocket: WebSocket):
        user = self.connected_clients.pop(websocket, None)
        await self.broadcast(message=f"{user['username']} left the chat", user=self.system_user)

    async def message(self, websocket: WebSocket, message: str):
        user = self.connected_clients[websocket]
        await self.broadcast(message=message, user=user)
        await self.history.add(self.unique_id, user, message)

    async def broadcast(self, message: str, user: dict):
        for connection in self.connected_clients:
            await self.send(connection, message, user)

    async def send(self, websocket: WebSocket, message: str, user: dict):
        response = self.create_response(user, message)
        await websocket.send_text(json.dumps(response))

    async def load_history(self, websocket: WebSocket):
        history = await self.history.get_list(self.unique_id)

        for user in history:
            await self.send(websocket, user['message'], user)

    @staticmethod
    def create_response(user, text):
        return ChatSchema(data=ChatDataSchema(author=user["username"], text=text, color=user["color"])).dict()


websocket_manager = WebSocketManager()
