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


@app.websocket("/room/{room_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    room_id: str,
    user_id: str,
):
    await manager.connect(websocket)
    conn = Connection(
        websocket=websocket,
        room_id=room_id,
        user_id=user_id)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{room_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{room_id} left the chat")