import threading


import json

import socket
from app.utils.CommonUtils import *
from app.route.cq_service import log_content_update
from app.settings import DefaultConfig
from app.utils.LoggerManager import logger 


class M2LoggerServer(threading.Thread):
    def __init__(self,address=(DefaultConfig.LOGGER_SERVICE_LISTEN_HOST,DefaultConfig.LOGGER_SERVICE_LISTEN_PORT)):
        super(M2LoggerServer,self).__init__()
        self.logger = logger
        self.session = []
        self.address = address
        self.logger.info("🛠️ TCP服务器初始化完成")


    def run(self):
        
        self.tcp_thread = threading.Thread(target=self.tcp_socket)
        self.tcp_thread.start()
        self.logger.info(f"tcp server listen on {self.address[0]}:{str(self.address[1])}")
    def tcp_socket(self):
        # 创建 TCP 套接字
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 设置套接字选项，允许地址重用
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # 绑定主机和端口
        self.server_socket.bind(self.address)

        # 开始监听
        self.server_socket.listen()
    
        try:
            while True:
                
                # 接受客户端连接
                client_socket, client_address = self.server_socket.accept()
                # 为每个客户端连接创建一个新的线程来处理
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
                client_thread.start()
                tmp_session_info = {
                    'socket':client_socket,
                    'adderss':client_address,
                    'thread':client_thread,
                    'uid':-1
                }
                self.session.append(tmp_session_info)
        except KeyboardInterrupt:
            print("Server shutting down...")
        finally:
            # 关闭服务器套接字
            self.server_socket.close()
        

    # 处理客户端连接的函数
    def handle_client(self,client_socket, client_address):
        # from app.extensions import client

        self.logger.info(f"Accepted connection from {client_address}")
        try:
            is_packet = False
            while True:

                # 接收客户端发送的数据
                data = client_socket.recv(8192)
                if not data:
                    break
                # CommonUtils.hex_dump(logger.info,data)
                try:
                    json_arr = self.decode_data_bin(data)
                    for e in json_arr:
                        # self.logger.info(f"{e['dCreateTime'].replace("\'","")}  {e['sReserve']}")
                        log_content_update(f"{e['dCreateTime'].replace("\'","")}  {e['sReserve']}")
                        CommonUtils.format_json_log(logger.info,e)
                        message = [
                            {
                                'type':'text',
                                'data':{
                                    'text':f"{e['dCreateTime'].replace("\'","")}  {e['sReserve']}"
                                }
                            }
                        ]
                        # qqrobot.send_private_msg("2210048995",message =message)
                        # qqrobot.send_group_msg("179614827",message =message)

                except Exception as e:
                    pass

        except Exception as e:
            self.logger.info(f"Error handling client {client_address}: {e}")
        finally:
            # 关闭客户端连接
            client_socket.close()
            self.logger.info(f"Connection with {client_address} closed")


    def decode_data_bin(self,data):
        # 定义JSON数据的起始标记和结束标记
        START_MARKER = b'04132'  # 对应字节 30 34 31 33 32
        START_MARKER_2=b'02000'
        END_MARKER = b'\x00'     # 空字节
        
        json_list = []
        current_pos = 0
        
        # 循环查找所有JSON数据块
        while True:
            # 查找下一个JSON起始标记
            start_pos = data.find(START_MARKER, current_pos)
            if start_pos == -1:
                start_pos = data.find(START_MARKER_2, current_pos)
                break  # 没有更多JSON数据
            
            # 计算JSON数据的起始位置（跳过标记本身）
            json_start = start_pos + len(START_MARKER)
            
            # 查找对应的结束标记
            end_pos = data.find(b"\x0a\x0d", json_start)
            
            if end_pos == -1:
                end_pos = data.find(b"\x00", json_start)
                if end_pos == -1:
                    break  # 没有找到结束标记，数据可能不完整
            
            # 提取JSON字节数据
            json_bytes = data[json_start:end_pos]
            
            # 尝试使用不同编码解析JSON
            parsed = None
            for encoding in ['gbk', 'utf-8', 'latin-1','gb2312']:
                try:
                    json_str = json_bytes.decode(encoding)
                    parsed = json.loads(json_str)
                    break  # 成功解析后跳出编码循环
                except (UnicodeDecodeError, json.JSONDecodeError):
                    continue  # 尝试下一种编码
            
            # 如果成功解析，添加到结果列表
            if parsed is not None:
                json_list.append(parsed)
            
            # 更新当前位置，继续查找下一个JSON块
            current_pos = end_pos + 1
        
        if len(json_list) == 0 :
            pass        
        return json_list
    # def parse_http_header(self,data):
    #     header_end = data.find(b'\r\n\r\n')
    #     if header_end == -1:
    #         # 头部不完整，需要继续读取
    #         return None
    #     header = data[:header_end]
    #     body = data[header_end + 4:]  # 跳过 \r\n\r\n
    #     return header, body
