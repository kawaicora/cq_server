# -*- coding:utf-8 -*-
import os,sys

from sqlalchemy import URL
class DefaultConfig (object):
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"  # 转换为布尔值（.env 中是字符串）
    USE_X_SENDFILE = False
    TRUSTED_HOSTS = None
    SERVER_NAME = os.getenv("SERVER_NAME")
    APPLICATION_ROOT = os.getenv("BASE_DIR", os.getcwd())  # 从 .env 读取，默认 os.getcwd()
    MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH", 4294967296))  # 转换为整数

    TEMPLATES_AUTO_RELOAD = os.getenv("TEMPLATES_AUTO_RELOAD", "True").lower() == "true"
    MAX_COOKIE_SIZE = int(os.getenv("MAX_COOKIE_SIZE", 4093))
    M2_SERVICE_ADDRESS_ARR = os.getenv("M2_SERVICE_ADDRESS").split(":")
    M2_SERVICE_ADDRESS = (M2_SERVICE_ADDRESS_ARR[0],int(M2_SERVICE_ADDRESS_ARR[1]))

    db_params = {
        "drivername":os.getenv("M2_DATABASE_DRIVER_NAME","mssql+pyodbc") ,
        "username": os.getenv("M2_DATABASE_USER"),
        "password": os.getenv("M2_DATABASE_PWD"),  # 若密码含特殊字符（如@），无需手动转义，URL对象会自动处理
        "host": os.getenv("M2_DATABASE_HOST","127.0.0.1"),    # 替换为你的实际数据库IP（之前的127.0.0.1/101.37.255.120）
        "port": int(os.getenv("M2_DATABASE_PORT",1433)),
        "database": os.getenv("M2_DATABASE_DB_NAME"),
        "query": {"driver": "ODBC Driver 17 for SQL Server"}  # 驱动名称直接写空格，无需转义
    }

    # 构建 URL 对象（核心：避免字符串解析错误）
    db_url = URL.create(**db_params)
    M2_DATABASE  = os.getenv("M2_DATABASE_URL")
    LOGGER_SERVICE_LISTEN_HOST=os.getenv("LOGGER_SERVICE_LISTEN_HOST","0.0.0.0")
    LOGGER_SERVICE_LISTEN_PORT=int(os.getenv("LOGGER_SERVICE_LISTEN_PORT",10000))
    #############传奇数据库
    SDK_BASE_URL = os.getenv("SDK_BASE_URL")
    BASE_DIR = os.getenv("BASE_DIR", os.getcwd())
    
    # 静态文件夹的路径
    STATIC_FOLDER = os.getenv("STATIC_FOLDER","static")
    TEMPLATES_FOLDER = os.getenv("TEMPLATES_FOLDER","templates")
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER","static/upload/")
    SQLALCHEMY_ECHO = os.getenv("SQLALCHEMY_ECHO", "False").lower() == "true"
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS", "False").lower() == "true"