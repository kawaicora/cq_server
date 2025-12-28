
from flask import Response
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from engineio.payload import Payload

# 提高单个 payload 允许的最大数据包数量（默认 16）

Payload.max_decode_packets = 1024
# db:SQLAlchemy = SQLAlchemy()
socketio:SocketIO = SocketIO(cors_allowed_origins='*',async_mode='gevent')


def set_cookies(response :Response,cookies,age:int = 24* 3600*30):
    for k,v in cookies.items():
        response.set_cookie(k,str(v))
    return response

