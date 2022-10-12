import os
import logging
from typing import Any
from fastapi import FastAPI, Body, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

import boto3

AWS_ACCESS_KEY_ID=os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY=os.environ['AWS_SECRET_ACCESS_KEY']
API_GATEWAY_ENDPOINT = os.environ['API_GATEWAY_ENDPOINT']

class ConnectionManager:

    def __init__(self):
        self.connection_ids = []
        self.gateway_api = boto3.client(
            'apigatewaymanagementapi',
            endpoint_url=API_GATEWAY_ENDPOINT,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name='ap-northeast-2'
        )
    
    def connect(self, conn: str):
        self.connection_ids.append(conn)

    def disconnect(self, conn: str):
        self.connection_ids.remove(conn)

    def send_message(self, message: dict, conn: str):
        self.gateway_api.post_to_connection(
            Data=message,
            ConnectionId=conn,
        )

    def broadcast(self, message: dict):
        for conn in self.connection_ids:
            self.send_message(message, conn)


app = FastAPI()
connection_manager = ConnectionManager()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
	exc_str = f'{exc}'.replace('\n', ' ').replace('   ', ' ')
	logging.error(f"{request}: {exc_str}")
	content = {'status_code': 10422, 'message': exc_str, 'data': None}
	return JSONResponse(content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


@app.put("/connect")
async def connect(
    connection_id: str = Body(),
    body: dict = Body(),
    params: str = Body(),
):
    connection_manager.connect(conn=connection_id)
    print(connection_id, body, params)
    return {"msg":"connected", "connection_id": connection_id}


@app.delete("/disconnect")
async def disconnect(
    connection_id: str = Body(),
    body: dict = Body(),
    params: str = Body(),
):
    connection_manager.disconnect(conn=connection_id)
    print(connection_id, body, params)
    return {"msg":"disconnected", "connection_id": connection_id}


@app.get('/default')
async def default():
    return {"msg": "Hello, This is Default route."}


@app.post('/send-message')
async def send_message(
    connection_id: str = Body(),
    body: dict = Body(),
):
    connection_manager.broadcast(
        message=body['message'],
    )
    print(connection_id, body, params)
    return {'msg':'send-message accepted'}