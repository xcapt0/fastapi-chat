import json
from starlette.websockets import WebSocketDisconnect, WebSocket

from .schema import ChatDataSchema, ChatSchema


class WebSocketManager:
    def __init__(self):
        self.connected_clients = set()

    def create_response(self, author, text):
        chat_data = ChatDataSchema(author=author, text=text)
        return ChatSchema(data=chat_data).dict()

    async def connect_websocket(self, websocket: WebSocket):
        await websocket.accept()
        self.connected_clients.add(websocket)

        response = self.create_response("Anonymous", "Connected")
        await websocket.send_text(json.dumps(response))

        try:
            while True:
                data = await websocket.receive_text()

                for client in self.connected_clients:
                    response = self.create_response("bla", data)
                    await client.send_text(json.dumps(response))
        except WebSocketDisconnect:
            self.connected_clients.remove(websocket)


websocket_manager = WebSocketManager()
