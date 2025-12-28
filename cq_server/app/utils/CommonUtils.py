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
    def gen_ticket(info:str = ""):
        a = secrets.token_hex(8).encode()
        b = info.encode()
        c =  str(datetime.timestamp(datetime.now()) ).encode()
        d = a + b+c
        e = base64.b16encode(d).decode().lower()
       
        return e
    @staticmethod
    def gen_order_no():
        n = "JAF"
        for i in range(28):
            
            n=n+ str(random.randint(0,9))
        return n

    @staticmethod
    def get_suffix_by_mimetype(mimetype: str) -> str:
        # MIME 类型到文件扩展名的映射
        mimetype_to_extension = {
            "image/jpeg": ".jpg",
            "image/png": ".png",
            "image/gif": ".gif",
            "image/bmp": ".bmp",
            "image/webp": ".webp",
            "image/tiff": ".tiff",
            "image/vnd.microsoft.icon": ".ico",
            "image/svg+xml": ".svg",
        }
        # 返回对应的扩展名，如果未找到则返回空字符串
        return mimetype_to_extension.get(mimetype.lower(), "")
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
    @staticmethod
    def cookies_str_to_dict (cookies_str:str)->dict:
        # 将cookies字符串分割成独立的键值对
        cookie_pairs = cookies_str.split(';')

        # 创建一个字典来存储cookies
        cookies_dict = {}
        for pair in cookie_pairs:
            # 去除空格并分割键和值
            key, value = pair.strip().split('=', 1)
            # 如果值是URL编码的，则进行解码
            value = unquote(value)
            # 将键值对添加到字典中
            cookies_dict[key] = value

        return cookies_dict
    @staticmethod
    def cookies_dict_to_str (cookies_dict:dict)->str:
        kv_list = []
        for key,value in cookies_dict.items():
            kv = []
            if not value:
                value = ""
            if isinstance(value, bool):
                value = str(value).lower()
            if isinstance(value, int):
                value = str(value)
            kv.append(key)
            kv.append(value)
            kv_list.append("=".join(kv)) 
        kv_str = ";".join(kv_list)
        return kv_str
    



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
    def get_time_of_day() -> str:
        # 获取当前时间
        current_time = datetime.now()
        # 获取当前小时数
        hour = current_time.hour

        # 根据小时数判断时间段
        if 5 <= hour < 10:
            return '早上'
        elif 10 <= hour < 12:
            return '上午'
        elif 12 < hour < 18:
            return '下午'
        elif 12 == hour:
            return '中午'
        else:
            return '晚上'   
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
    def gen_verify_code(len:int=6)->int:
        """
        生成指定长度的验证码
        """
        return ''.join(random.choices('0123456789', k=len))
    def send_verify_code(email:str,verify_url:str = ''):
        from app.settings import DefaultConfig
        # 创建 Jinja2 环境
        env = Environment(loader=FileSystemLoader("."))
 
        # 生成验证码
        verify_code = CommonUtils.gen_verify_code()
        # 加载模板文件
        template = env.get_template('templates/verify_code.html')
        # 定义要替换的变量
        data = {
            'verify_url': verify_url,
            'verify_code': verify_code
        }

        # 渲染模板
        output = template.render(data)

      
        CommonUtils.send_mail_exa(email,output)
        return data
    
    ##############################################################################################################
    @staticmethod 
    def send_mail_exa(receiver,html):
        from app.settings import DefaultConfig
        
        import resend
        
        resend.api_key = "re_TzTwmfdX_NdW52Ak9uZezLc3TmfhQqWbq"

        params: resend.Emails.SendParams = {
        "from": f"admin@st.org",
        "to": [receiver],
        "subject": '这是你的验证码',
        "html": html
        }

        email = resend.Emails.send(params)
        
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
        
    ######################################################异步方法#############################################
    @staticmethod

    def __ensure_event_loop() -> None:
        try:
            asyncio.get_event_loop()

        except:
            asyncio.set_event_loop(asyncio.new_event_loop())

    @staticmethod
    def sync(coroutine: Coroutine[Any, Any, T]) -> T:
        """
        同步执行异步函数，使用可参考 [同步执行异步代码](https://nemo2011.github.io/bilibili-api/#/sync-executor)

        Args:
            coroutine (Coroutine): 异步函数

        Returns:
            该异步函数的返回值
        """
        CommonUtils.__ensure_event_loop()
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(coroutine)
    ######################################################密码与验证#############################################
    @staticmethod
    def password_to_hash(password: str) -> str:
        """
        将明文密码转换为哈希值字符串。
        该方法会生成一个随机盐值，并使用 Scrypt 算法对密码进行哈希处理。
        最终返回的哈希值包含盐值和经过哈希处理后的密码，以 Base64 编码的字符串形式存储。

        :param password: 明文密码，字符串类型。
        :return: 包含盐值和哈希密码的 Base64 编码字符串。
        """
        # 生成随机盐值
        salt = os.urandom(16)
        # 创建 Scrypt 密钥派生函数实例
        kdf = Scrypt(
            salt=salt,
            length=32,
            n=2 ** 14,
            r=8,
            p=1,
            backend=default_backend()
        )
        # 对密码进行哈希处理
        hashed = kdf.derive(password.encode())
        # 组合盐值和哈希密码
        combined = salt + hashed
        # 以 Base64 编码为字符串
        return base64.b64encode(combined).decode()

    @staticmethod
    def verify_password(password: str, hashed_password_str: str) -> bool:
        """
        验证输入的明文密码是否与存储的哈希密码匹配。
        该方法会从存储的 Base64 编码的哈希密码中提取盐值，
        然后使用相同的 Scrypt 算法对输入的密码进行哈希处理，
        最后比较两个哈希值是否相同。

        :param password: 明文密码，字符串类型。
        :param hashed_password_str: 存储的包含盐值和哈希密码的 Base64 编码字符串。
        :return: 如果密码匹配返回 True，否则返回 False。
        """
        # 解码 Base64 字符串为字节
        hashed_password = base64.b64decode(hashed_password_str)
        # 从存储的哈希密码中提取盐值
        salt = hashed_password[:16]
        stored_hash = hashed_password[16:]
        # 创建 Scrypt 密钥派生函数实例
        kdf = Scrypt(
            salt=salt,
            length=32,
            n=2 ** 14,
            r=8,
            p=1,
            backend=default_backend()
        )
        try:
            # 对输入的密码进行哈希处理并验证
            kdf.verify(password.encode(), stored_hash)
            return True
        except Exception:
            return False
    @staticmethod
    def remove_key_recursive(obj, target_key):
        if isinstance(obj, dict):
            # 删除当前层级的键
            if target_key in obj:
                del obj[target_key]
            # 递归处理所有值
            for key in list(obj.keys()):  # 转换为list避免字典改变导致的遍历错误
                CommonUtils.remove_key_recursive(obj[key], target_key)
        elif isinstance(obj, list):
            # 递归处理列表中的每个元素
            for item in obj:
                CommonUtils.remove_key_recursive(item, target_key)

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
        

    ##########################################################################################
    @staticmethod
    def create_rsa_key(key_size=2048,public_exponent=65537):
        """
        创建RSA密钥
        返回 私钥,公钥
        """
        # 生成 RSA 私钥
        private_key = rsa.generate_private_key(
            public_exponent=65537,  # 公共指数，通常使用 65537
            key_size=2048,  # 密钥长度，建议使用 2048 或更高
            backend=default_backend()
        )

        # 从私钥中提取公钥
        public_key = private_key.public_key()

        # 将私钥序列化为 PEM 格式
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )

        # 将公钥序列化为 PEM 格式
        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return private_pem,public_pem
    @staticmethod 
    def get_exist_rsa_key(pem_path:str = None,create_new:bool = True):
        """
        从已有的私钥和公钥中加载RSA密钥
        返回 私钥,公钥
        """
        
        from app.settings import DefaultConfig 

        if pem_path is None:
            pem_path = DefaultConfig.PASSWORD_PRIVATE_KEY_FILE

        if os.path.exists(pem_path) :
            with open(pem_path, "rb") as f:
                private_pem = f.read()
                private_key = CommonUtils.load_private_key(private_pem)
                # 从私钥中提取公钥
                public_key = private_key.public_key()
                # 将公钥序列化为 PEM 格式
                public_pem = public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo
                )
                return private_pem,public_pem
        else:
            if(create_new):
                private_pem,public_pem = CommonUtils.create_rsa_key()
                with open(pem_path, "wb") as f:
                    f.write(private_pem)
                return private_pem,public_pem

        
    @staticmethod
    def load_private_key(private_pem: str | bytes,password:bytes = None):
        # 判断 private_pem 的类型
        if isinstance(private_pem, str):
            private_pem = private_pem.encode()
        # 加载 PEM 格式私钥文本到私钥对象
        try:
            private_key = serialization.load_pem_private_key(
                private_pem,
                password=password,
                backend=default_backend()
            )
            return private_key
        except Exception as e:
            return None
        
    @staticmethod
    def load_public_key(public_pem: str | bytes):
        # 判断 private_pem 的类型
        if isinstance(public_pem, str):
            public_pem = public_pem.encode()
        # 加载 PEM 格式私钥文本到私钥对象
        try:
            public_key = serialization.load_pem_public_key(
                public_pem,
                backend=default_backend()
            )
            return public_key
        except Exception as e:
            return None
    @staticmethod
    def aes_encrypt_large_data(data, key):
        """
        加密大数据
        :param data: 待加密的数据（bytes 类型）
        :param key: 加密密钥（bytes 类型，长度可以是 16、24 或 32 字节）
        :return: 加密后的数据（bytes 类型）和初始化向量（IV）
        """
        # 生成一个随机的初始化向量（IV），AES 在 CBC 模式下需要 IV
        iv = os.urandom(16)
        # 创建 AES 加密器，使用 CBC 模式
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()

        # 对数据进行填充，使其长度为 16 字节的倍数
        block_size = 16
        padding_length = block_size - (len(data) % block_size)
        padded_data = data + bytes([padding_length]) * padding_length

        encrypted_chunks = []
        # 分块加密数据
        for i in range(0, len(padded_data), block_size):
            chunk = padded_data[i:i + block_size]
            encrypted_chunk = encryptor.update(chunk)
            encrypted_chunks.append(encrypted_chunk)

        # 完成加密过程
        final_chunk = encryptor.finalize()
        encrypted_chunks.append(final_chunk)

        encrypted_data = b''.join(encrypted_chunks)
        return encrypted_data, iv
    @staticmethod
    def aes_decrypt_large_data(encrypted_data, key, iv):
        """
        解密大数据
        :param encrypted_data: 加密后的数据（bytes 类型）
        :param key: 解密密钥（bytes 类型，与加密时的密钥相同）
        :param iv: 初始化向量（IV，bytes 类型）
        :return: 解密后的数据（bytes 类型）
        """
        # 创建 AES 解密器，使用 CBC 模式
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_chunks = []
        block_size = 16
        # 分块解密数据
        for i in range(0, len(encrypted_data), block_size):
            chunk = encrypted_data[i:i + block_size]
            decrypted_chunk = decryptor.update(chunk)
            decrypted_chunks.append(decrypted_chunk)

        # 完成解密过程
        final_chunk = decryptor.finalize()
        decrypted_chunks.append(final_chunk)

        decrypted_data = b''.join(decrypted_chunks)
        # 去除填充数据
        padding_length = decrypted_data[-1]
        decrypted_data = decrypted_data[:-padding_length]
        return decrypted_data
    

    @staticmethod
    # 获取RSA加密块的最大大小，考虑填充方式
    def get_max_chunk_size(key_size: int, padding_scheme: str = "PKCS1v15"):
        key_bytes = key_size // 8
        if padding_scheme == "OAEP":
            # OAEP 填充需要额外的字节，SHA-256 的 hash_size 是 32 字节
            hash_size = 32
            padding_overhead = 2 * hash_size + 2
        else:  # 默认使用 PKCS#1 v1.5 填充
            padding_overhead = 11  # PKCS#1 v1.5 填充的标准字节大小为 11 字节
        
        # 最大数据块大小：RSA密钥大小减去填充的大小
        max_chunk_size = key_bytes - padding_overhead
        return max_chunk_size

    @staticmethod
    # RSA 分块加密，支持选择填充方式
    def rsa_encrypt_chunks(data: bytes, public_key, padding_scheme: str = "PKCS1v15"):
        key_size = public_key.key_size
        max_chunk_size = CommonUtils.get_max_chunk_size(key_size, padding_scheme)
        encrypted_chunks = []

        for i in range(0, len(data), max_chunk_size):
            chunk = data[i:i + max_chunk_size]

            if padding_scheme == "OAEP":
                encrypted_chunk = public_key.encrypt(
                    chunk,
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                )
            else:  # 默认使用 PKCS#1 v1.5 填充
                encrypted_chunk = public_key.encrypt(
                    chunk,
                    padding.PKCS1v15()
                )

            encrypted_chunks.append(encrypted_chunk)

        return b''.join(encrypted_chunks)

    @staticmethod
    # RSA 分块解密，支持选择填充方式
    def rsa_decrypt_chunks(encrypted_data: bytes, private_key, padding_scheme: str = "PKCS1v15"):
        key_size = private_key.key_size
        chunk_size = key_size // 8  # 这应该等于RSA密钥的字节大小
        decrypted_chunks = []

        for i in range(0, len(encrypted_data), chunk_size):
            chunk = encrypted_data[i:i + chunk_size]

            if padding_scheme == "OAEP":
                decrypted_chunk = private_key.decrypt(
                    chunk,
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                )
            else:  # 默认使用 PKCS#1 v1.5 填充
                decrypted_chunk = private_key.decrypt(
                    chunk,
                    padding.PKCS1v15()
                )

            decrypted_chunks.append(decrypted_chunk)

        return b''.join(decrypted_chunks)

    @staticmethod
    # 对数据进行哈希计算
    def hash_data(data):
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        if isinstance(data, bytes):
            digest.update(data)
        elif isinstance(data, str):
            digest.update(data.encode())
        return digest.finalize()

    @staticmethod
    # RSA 签名
    def rsa_sign(private_key, data):
        hash_value = CommonUtils.hash_data(data)
        signature = private_key.sign(
            hash_value,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return signature

    @staticmethod
    # RSA 验证签名
    def rsa_verify(public_key, data, signature):
        hash_value = CommonUtils.hash_data(data)
        try:
            public_key.verify(
                signature,
                hash_value,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except Exception:
            return False
