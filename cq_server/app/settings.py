# -*- coding:utf-8 -*-
import os,sys
class DefaultConfig (object):

    M2_SERVICE_ADDRESS = ("127.0.0.1",6999)
    SDK_BASE_URL = "http://10.0.0.10:5500"
    M2_DATABASE  = (
        "mssql+pyodbc://sa:mssql_HPNwE4@127.0.0.1:1433/dhsf_stcq_9762_game_9306444_mdf?"
        "driver=ODBC+Driver+17+for+SQL+Server"
    )   #############传奇数据库
    BASE_DIR = os.getcwd() # 项目根目录
    DEBUG = True # 是否开启调试模式
    MAX_CONTENT_LENGTH = 4096 * 1024 * 1024 # 4GB
    # 静态文件夹的路径
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER ='templates'
    UPLOAD_FOLDER = "static/upload/"
    TEMPLATES_AUTO_RELOAD = True # 模板自动加载
    SQLALCHEMY_ECHO = False # 是否开启SQLAlchemy的调试模式
    SQLALCHEMY_TRACK_MODIFICATIONS = False # 是否追踪对象的修改
    PASSWORD_PRIVATE_KEY_FILE = "data/password_private_key.pem"
 