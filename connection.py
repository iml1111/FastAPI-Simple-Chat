from typing import List, Dict
from fastapi import WebSocket
from pydantic import BaseModel
from collections import defaultdict


class Connection(BaseModel):
    websocket: WebSocket
    room_id: str
    user_id: str


class ConnectionManager:
    def __init__(self):
        self.connection_dict: Dict[str, List[Connection]] = defaultdict(list)

    async def connect(self, conn: Connection):
        await conn.websocket.accept()
        self.connection_dict[conn.room_id].append(conn)

    def disconnect(self, conn: Connection):
        self.connection_dict[conn.room_id].remove(conn)

    async def send_personal_message(
        self,
        message: str,
        conn: Connection
    ):
        await conn.websocket.send_text(message)

    async def broadcast(self, message: str):
        """All broadcast"""
        for room in self.connection_dict:
            for conn 
        for connection in self.active_connections:
            await connection.send_text(message)


connection_manager = ConnectionManager()
