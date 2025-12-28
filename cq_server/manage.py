# -*- coding:utf-8 -*-

import threading
from app import app, socketio,logger
from app.utils.M2LoggerServer import M2LoggerServer
import warnings
from loguru import logger
warnings.filterwarnings("ignore", category=RuntimeWarning, module="google_crc32c")

if __name__ == "__main__":
    try:
        M2LoggerServer().start()
        # 使用 eventlet 作为后端服务器
        socketio.run(
            app, 
            host="0.0.0.0", 
            port=5500, 
            debug=True, 
            use_reloader=False,
            allow_unsafe_werkzeug=True  # 允许在异步模式下使用调试功能
        )
    except Exception as e:
        logger.error(f"Failed to start server : {str(e)}")