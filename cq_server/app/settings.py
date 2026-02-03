# -*- coding:utf-8 -*-
import os,sys
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
    M2_DATABASE  = os.getenv("M2_DATABASE_URL")
        
   #############传奇数据库
    SDK_BASE_URL = os.getenv("SDK_BASE_URL")
    BASE_DIR = os.getenv("BASE_DIR", os.getcwd())
    
    # 静态文件夹的路径
    STATIC_FOLDER = os.getenv("STATIC_FOLDER","static")
    TEMPLATES_FOLDER = os.getenv("TEMPLATES_FOLDER","templates")
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER","static/upload/")
    SQLALCHEMY_ECHO = os.getenv("SQLALCHEMY_ECHO", "False").lower() == "true"
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS", "False").lower() == "true"