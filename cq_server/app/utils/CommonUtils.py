import hashlib
import asyncio
import os
import string
import time
from typing import Any, TypeVar, Coroutine
import base64
import secrets
from datetime import datetime
import hashlib
import json
from urllib.parse import quote, quote_plus,unquote,unquote_plus
import random
import smtplib
from email.mime.text import MIMEText
from email.header import Header

from cryptography.hazmat.primitives.asymmetric import rsa,padding
from cryptography.hazmat.primitives import serialization
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from flask import Response
from jinja2 import Environment, FileSystemLoader
import rarfile
import zipfile
T = TypeVar("T")
class CommonUtils:
    
    @staticmethod
    def gen_order_no():
        n = "JAF"
        for i in range(28):
            
            n=n+ str(random.randint(0,9))
        return n

  
    @staticmethod
    def create_directory(path):
        """
        递归创建文件夹，如果文件夹已存在则不会报错。
        """
        try:
            os.makedirs(path, exist_ok=True)
            return True
        except Exception as e:
            return False
    @staticmethod
    def calculate_md5(input_data, encoding='utf-8'):
        # 如果输入是字符串，则先编码为字节
        if isinstance(input_data, str):
            input_data = input_data.encode(encoding)
        
        # 使用Python的hashlib库计算MD5哈希
        md5_hash = hashlib.md5()
        md5_hash.update(input_data)
        
        # 返回十六进制表示的哈希值
        return md5_hash.hexdigest()
    @staticmethod
    def random_number(len=19):
        out = ""
        for i in range(len):
            out += str(random.randint(0,9))
        return out

    @staticmethod
    def sort_para_to_str(para:str|list,split_suffix = '&',ignore_empty_value:bool = True):
        if isinstance(para,str):
            para:dict = CommonUtils.para_to_dict(para,ignore_empty_value)
        tmp =  []
        for k,v in para.items():
            if (ignore_empty_value):
                if v != '':
                    tmp.append(f'{k}={quote(str(v))}')
            else:
                tmp.append(f'{k}={v}')

        a = sorted(tmp,reverse=False)

        return split_suffix.join(a)
    
    @staticmethod
    def random_string(len=64):
        chat_set = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        return ''.join(random.choices(chat_set, k=len))
    
    @staticmethod
    def para_to_dict(para:str,ignore_empty_value:bool = True):
        tmp = {}
        para_kv_list = para.split("&")
        for item in para_kv_list:
            if ignore_empty_value :
                if(item.split('=')[1] != ''):
                    tmp[item.split('=')[0]] = item.split('=')[1]
            else:
                tmp[item.split('=')[0]] = item.split('=')[1]
        return tmp
    @staticmethod
    def dict_to_params(data):
        """
        把字典转换为URL查询字符串格式，并且进行URL编码
        :param data: 原始字典
        :return: 转换后的URL查询字符串
        """
        # 用于存储转换后的键值对
        param_list = []
        # 遍历字典中的每个键值对
        for key, value in data.items():
            # 如果值是字典或者列表，就先转成JSON字符串
            if isinstance(value, (dict, list)):
                value = json.dumps(value)
            # 把键和值进行URL编码，然后添加到列表中
            param_list.append(f"{quote(str(key))}={quote(str(value))}")
        # 用&符号连接所有键值对
        return '&'.join(param_list)




    # 辅助函数
    @staticmethod
    def quote_special_chars(s):
        # 简化的urlencode实现
        return s.replace(' ', '+').replace('&', '%26').replace('=', '%3D')
    @staticmethod
    def generate_random_id(prefix):
        # 生成随机字符串，类似Lua的randDataID
        characters = string.ascii_letters + string.digits
        random_part = ''.join(random.choice(characters) for i in range(10))
        return f"{prefix}{random_part}"



    @staticmethod
    
    def calc_cloud_sign_suffix(origin_data, secret_key, urlencode=False):
        # 按key排序
        sorted_data = sorted(origin_data, key=lambda x: x['key'])
        
        # 拼接参数
        origin = ""
        value_str = ""
        for item in sorted_data:
            if item and 'key' in item and 'value' in item and \
            len(item['key']) > 0 and len(item['value']) > 0:
                key = item['key']
                value = item['value']
                if urlencode:
                    # 简化的urlencode实现，实际使用中建议用urllib.parse.quote
                    value = CommonUtils.quote_special_chars(value)
                origin += f"{key}={value}&"
                value_str += value
        
        # 移除最后一个&
        if origin.endswith('&'):
            origin = origin[:-1]
        
        rqtime = int(time.time())
        rqrandom = CommonUtils.generate_random_id("Box")
        value_str += f"{secret_key}{rqtime}{rqrandom}"
        print(f"isCloudLogin : RequestIsCloudLogin {value_str}")
        
        # 计算MD5签名
        sign_md5 = hashlib.md5(value_str.encode('utf-8')).hexdigest()
        
        # 构建结果字典
        result = {item['key']: item['value'] for item in origin_data}
        result.update({
            'rqtime': rqtime,
            'rqrandom': rqrandom,
            'sign': sign_md5
        })
        return result
    @staticmethod
    def verify_cloud_sign(params, secret_key):
        # 提取签名和动态参数
        if 'sign' not in params or 'rqtime' not in params or 'rqrandom' not in params:
            return False
        
        original_sign = params.pop('sign')
        rqtime = params.pop('rqtime')
        rqrandom = params.pop('rqrandom')
        
        # 排序参数
        sorted_params = sorted(params.items(), key=lambda x: x[0])
        
        # 拼接值字符串
        value_str = ''.join([str(value) for _, value in sorted_params])
        value_str += f"{secret_key}{rqtime}{rqrandom}"
        
        # 计算验证签名
        expected_sign = hashlib.md5(value_str.encode('utf-8')).hexdigest()
        
        return original_sign == expected_sign


    @staticmethod 
    def process_json_only_string(input):
        # 使用列表推导式来遍历列表中的每个字典，并转换布尔值为字符串
        contents_as_strings = [
            {key: str(value).lower() if isinstance(value, bool) else str(value) for key, value in item.items()}
            for item in input
        ]

        # 打印结果
        return contents_as_strings
    def unzip_file(file_path, extract_path):
        try:
            if file_path.endswith('.zip'):
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    zip_ref.extractall(extract_path)
                print(f"成功解压 {file_path} 到 {extract_path}")
            elif file_path.endswith('.rar'):
                rf = rarfile.RarFile(file_path)
                rf.extractall(extract_path)
                print(f"成功解压 {file_path} 到 {extract_path}")
            else:
                print("不支持的压缩文件格式，请使用 ZIP 或 RAR 格式。")
        except Exception as e:
            print(f"解压过程中出现错误: {e}")
 
    @staticmethod
    def format_json(json_data,ensure_ascii=False) ->str:
        """
        格式化JSON
        返回 展开的JSON字符串
        """
        return json.dumps(json_data, indent=2,ensure_ascii=ensure_ascii)
    @staticmethod
    def format_json_log(callback ,json_data:dict) ->None:
        """
        使用传入的方法打印展开的JSON
        """
        callback(CommonUtils.format_json(json_data))
    @staticmethod
    def hex_dump(callback,data, width=16) ->None:
        """
        打印16进制数据 类似于go的hex.dump
        """
        msg = ""
        for i in range(0, len(data), width):
            chunk = data[i:i + width]
            hex_str = ' '.join(f"{byte:02X}" for byte in chunk)
            printable = ''.join(chr(byte) if 32 <= byte < 127 else '.' for byte in chunk)
            # 计算需要的填充空格数量
            padding = ' ' * ((width - len(chunk)) * 3)
            msg += f"{hex_str} {padding} | {printable}\n"
        callback(f"\n\n{msg}\n\n")

    @staticmethod
    
    

    @staticmethod
    def send_mail(smtp_server,port,username ,password,sender  ,receiver ,subject ,body,type,encoding='utf-8'):
        # CommonUtils.send_mail(
        #     smtp_server=DefaultConfig.SMTP_SERVER,
        #     port=DefaultConfig.SMTP_PORT,
        #     username=DefaultConfig.USERNAME,
        #     password=DefaultConfig.PASSWROD,
        #     sender=DefaultConfig.SENDER,
        #     receiver=email,
        #     subject='这是你的验证码',
        #     body=output,type='html')
        # 创建邮件正文
        message = MIMEText(body, type, encoding)
        message['From'] = Header(sender, encoding)
        message['To'] = Header(receiver, encoding)
        message['Subject'] = Header(subject, encoding)
        # 连接SMTP服务器
        server = smtplib.SMTP(smtp_server, port)
        server.login(username, password)
        # 发送邮件
        server.sendmail(username, receiver, message.as_string())
        # 断开连接
        server.quit()
        

    @staticmethod
    def json_response(json_data,cookies=None,headers=None):
        """
        返回json格式的响应
        """
        response = Response(json.dumps(json_data), content_type='application/json',headers=headers)
        if cookies:
            for key, value in cookies.items():
                response.set_cookie(key, value)
        return response
        


