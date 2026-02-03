# -*- coding:utf-8 -*-
import dotenv,os  # 导入 python-dotenv
dotenv.load_dotenv()

from app import app, socketio
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
            host=os.getenv("LISTEN_HOST","0.0.0.0"), 
            port=int(os.getenv("LISTEN_PORT",80)),
            debug=os.getenv("DEBUG",False), 
            use_reloader=False,
            allow_unsafe_werkzeug=True  # 允许在异步模式下使用调试功能
        )
    except Exception as e:
        logger.error(f"Failed to start server : {str(e)}")