import logging
from flask import Flask
from flask_cors import CORS
from app.utils.LoggerManager import logger
from app.route import bp as root
from app.settings import DefaultConfig
from app.extensions import socketio

# 创建 Flask 应用
app:Flask = Flask(__name__, 
           instance_relative_config=True,
           template_folder=DefaultConfig.TEMPLATES_FOLDER,
           static_folder=DefaultConfig.STATIC_FOLDER)

# 初始化日志管理器
app.logger = logger

# 加载配置文件
app.config.from_object(DefaultConfig)

# 设置路径信息
app.root_path = DefaultConfig.BASE_DIR
app.config['UPLOAD_FOLDER'] = DefaultConfig.UPLOAD_FOLDER

# 配置跨域支持
CORS(app, supports_credentials=True)

# 注册蓝图
app.register_blueprint(root)

# 初始化扩展

socketio.init_app(app)

# 创建数据库表
with app.app_context():
    try:
      
        logger.info("app_content")
    except Exception as e:
        logger.error(f"Failed to do app_content: {str(e)}")
