from typing import Union
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect, status
from fastapi.templating import Jinja2Templates
from connection import connection_manager as manager
from connection import Connection

app = FastAPI()
template_engine = Jinja2Templates(directory="templates")
templating = template_engine.TemplateResponse


@app.get("/")
async def index(request: Request):
    return templating("index.html", {"request": request})


@app.get('/room')
async def room():
    """Current online users"""
    online_room_info = {}
    for room in manager.connection_dict:
        online_room_info[room] = {}
        online_room_info[room]['member_len'] = len(manager.connection_dict[room])
        online_room_info[room]['members'] = [
            conn.user_id for conn in manager.connection_dict[room]
        ]
    return online_room_info


@app.websocket("/room/{room_id}/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    room_id: str,
    user_id: str,
):
    conn = Connection(
        websocket=websocket,
        room_id=room_id,
        user_id=user_id)
    await manager.connect(conn)
    try:
        while True:
            data = await websocket.receive_json()
            if data['type'] == 'message':
                await manager.multicast(
                    message={
                        "user_id": user_id,
                        "message": data['message'],
                        "type": "message",
                    },
                    room_id=room_id,
                )
            elif data['type'] == 'broadcast':
                await manager.broadcast(
                    message={
                        "room_id": room_id,
                        "user_id": user_id,
                        "message": data['message'],
                        "type": "broadcast",
                    },
                )
    except WebSocketDisconnect:
        manager.disconnect(conn)
        await manager.multicast(
            message={
                "user_id": user_id,
                "message": "left the room",
                "type": "system"
            },
            room_id=room_id,
        )
