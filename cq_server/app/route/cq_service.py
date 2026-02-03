# -*- coding:utf-8 -*-
import mimetypes
import shutil
import time
from app.utils.LoggerManager import logger
import qrcode
from qrcode.image.styledpil import StyledPilImage
from PIL import Image
import urllib.parse

import requests
from app.route import bp

from flask import *
from app.settings import *
from app.utils.CommonUtils import *
from app.utils.CommonUtils import CommonUtils
from app.utils.ErrorCode import get_response_string,get_response_json
from app.extensions import socketio
from app.settings import DefaultConfig
from decimal import Decimal
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
from app.sql_class.Legend import TBLBOXSELL, TBLCHARACTER, Pay,Diypay,TBLMAIL,t_TBL_CONFIG
from datetime import datetime
from app.utils.M2Service import *
order_data = {}


# 创建连接



engine = create_engine(DefaultConfig.M2_DATABASE)
# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def verify_user(token):
    # t_account = Account.query.filter_by(login_token=token).first()
    # if t_account :
    #     return True
    # return False
    return True
def log_content_update(data):
    socketio.emit('log_content_update',{"content":data})
    return


def send_mail(role_id:str,sender_name:str,lable:str,memo:str,item:str=''):
    if isinstance(item,dict) or isinstance(item,list):
        item = json.dumps(item,ensure_ascii=False)
    session: Session = SessionLocal()

    try:
        new_tblmail = TBLMAIL(
            UserID=role_id,
            SendName=sender_name,
            Type=Decimal(0),
            Lable=lable,
            Memo=memo,
            Item=item,
            dCreateTime=datetime.now(),
            RecvFlag = Decimal(0),
            ReadFlag = Decimal(0),
            Deleted = Decimal(0)
        )
    # 自动开始事务
        session.add(new_tblmail)
        session.commit()  # 自动flush + commit
        mail_notify(role_id)
        return 0
    
    except Exception as e:
        session.rollback()
        # logger.info(f"插入失败: {str(e)}")
    finally:
        session.close()
    return -1

def pay(server_id:str,account:str,role_id:str,amount:int,order_id:str,sdk_id:int=59098,draw_out:int = 0,ext_data:str=2,product_id:str="0",ext_id:int=2):
    session: Session = SessionLocal()
    try:
   
        new_pay: Pay = Pay(
            PayId=order_id,
            sGameOrder=order_id,
            sRoleId=role_id,
            Account=account,
            SdkId=sdk_id,
            ServerId=server_id,
            ProductId=product_id,
            Gold=Decimal(amount),  # 必须使用Decimal类型
            nRealGold=Decimal(amount),
            ExtData=ext_data,
            DrawOut=draw_out, #抽取状态 新订单为 0 不要设置DrawLevel和DrawDate
            CreateTime=datetime.now(),
            nExtid=ext_id, #货币ID
        )
        # 自动开始事务
        session.add(new_pay)
        session.commit()  # 自动flush + commit
        send_pay_notify(account,role_id)
        return 0
    
    except Exception as e:
        session.rollback()
        # logger.info(f"插入失败: {str(e)}")
    finally:
        session.close()
    return -1



def diypay(server_id:str,account:str,role_id:str,amount:int,order_id:str,sdk_id:int=59098,draw_out:int = 0,ext_data:str=2,product_id:str="0",ext_id:int=2):
    session: Session = SessionLocal()
    try:
   
        new_diypay : Diypay= Diypay(
            PayId=order_id,
            sGameOrder=order_id,
            sRoleId=role_id,
            Account=account,
            SdkId=sdk_id,
            ServerId=server_id,
            ProductId=product_id,
            Gold=Decimal(amount),  # 必须使用Decimal类型
            ExtData=ext_data,
            DrawOut=draw_out, #抽取状态 新订单为 0 不要设置DrawLevel和DrawDate
            CreateTime=datetime.now(),
            nExtid=ext_id, #货币ID
        )
        # 自动开始事务
        session.add(new_diypay)
        session.commit()  # 自动flush + commit
        send_diy_pay_notify(role_id)
        return 0
    
    except Exception as e:
        session.rollback()
        # logger.info(f"插入失败: {str(e)}")
    finally:
        session.close()
    return -1

# 2. 按 sRegionServerName 更新 recharge_config 的函数
def update_recharge_config_by_region(region_server_name: str, new_recharge_config: list[dict[str, Any]]):
    """
    根据服务器名称更新充值配置
    :param region_name: 目标服务器名称（对应 sRegionServerName 字段）
    :param new_recharge_config: 新的充值配置（字符串格式，建议 JSON 串）
    :return: 是否更新成功
    """
    db: Session = SessionLocal()
    try:
        # 定位目标记录：按 sRegionServerName 精确匹配
        target_config = db.query(t_TBL_CONFIG).filter(
            t_TBL_CONFIG.sRegionServerName == region_server_name
        ).first()

        if not target_config:
            logger.info(f"错误：未找到服务器名称为「{region_server_name}」的配置记录")
            return False

        # 更新 recharge_config 字段
        target_config.recharge_config = new_recharge_config
        # 可选：更新最后修改时间（若表中有对应字段，如 AddTime/UpdateTime）
        # target_config.UpdateTime = datetime.now()

        db.commit()  # 提交修改
        db.refresh(target_config)  # 刷新实例，获取最新数据
        logger.info(f"成功：服务器「{region_server_name}」的充值配置已更新")
        return True

    except Exception as e:
        db.rollback()  # 出错回滚，避免数据不一致
        logger.info(f"失败：更新充值配置时出错 - {str(e)}")
        return False

    finally:
        db.close()  # 无论成功与否，关闭会话

def add_tbl_config(region_server_name: str):
    session = SessionLocal()
    try:
        json_recharge_config: list[dict[str, Any]]= [
            {
                "currency_name":"元宝",
                "currency_ratio":10,
                "currency_itemid":2,
                "present_deploy":[],
                "point_deploy":[],
                "present_ratio":"",
                "per_pay_present":[]
            }
        ]
        json_serconfig = {
            "maxitemlog":1000,
            "maxdummy":50,
            "createservertime":1748658649,
            "testservertime":1748660400,
            "startservertime":1748664000,
            "limitchat":0,
            "limitjob":0
        }
        
        # 实例化配置记录（按需设置字段值，未设置的字段将使用默认值）
        new_config = t_TBL_CONFIG(
            StartTime=datetime.datetime.now(),  # 当前时间
            recharge_config=json.dumps(json_recharge_config),  # 充值配置（JSON字符串）
            Regis=0,  # 非空字段，必须赋值
            sRegionServerName=region_server_name,
            FLD_SERCONFIG = json.dumps(json_serconfig)
            
        )
        
        # 添加到会话并提交
        session.add(new_config)
        session.commit()
        
    except Exception as e:
        pass




    

default_ok = {"code":200,"msg":"操作成功","data": True,"success":True}

################################################管理页面############################################

@bp.route("/")
def index():
    return ""

@bp.route("/view/game_manager",methods=["GET"])
def view_game_manager():
    response = None
    if verify_user(request.cookies.get('token')):
        response = make_response(render_template("game_manager.html"),200)
    else:
        response =CommonUtils.json_response(get_response_json(-3005)) 
    if response:
        response.headers['X-Organization'] = 'Nintendo'
        return response
    else:
        return get_response_string(-1)
def get_userid_by_character(character: str) -> str | None:
    session = SessionLocal()
    try:
        result = session.query(TBLCHARACTER.FLD_USERID) \
            .filter(TBLCHARACTER.FLD_CHARACTER == character) \
            .first()
        session.close()
        return result[0] if result else None
    except Exception as e:
        return None
     
def get_account_by_userid(user_id: str) -> str | None:
    """通过用户ID从 TBL_CHARACTER 表中查询 FLD_ACCOUNT"""
    session = SessionLocal()
    try:
        result = session.query(TBLCHARACTER.FLD_ACCOUNT) \
            .filter(TBLCHARACTER.FLD_USERID == user_id) \
            .first()
        session.close()
        return result[0] if result else None
    except :
        return None
    
def get_server_id_by_userid(user_id: str) -> str | None:
    """通过用户ID从 TBL_CHARACTER 表中查询 FLD_SERVERID"""
    session = SessionLocal()
    try:
        result = session.query(TBLCHARACTER.FLD_SERVERID) \
            .filter(TBLCHARACTER.FLD_USERID == user_id) \
            .first()
        session.close()
        return result[0] if result else None
    except :
        return None
    
def get_sdk_id_by_userid(user_id: str) -> str | None:
    """通过用户ID从 TBL_CHARACTER 表中查询 FLD_SDKID"""
    session = SessionLocal()
    try:
        result = session.query(TBLCHARACTER.FLD_SDKID) \
            .filter(TBLCHARACTER.FLD_USERID == user_id) \
            .first()
        session.close()
        return result[0] if result else None
    except :
        return None
    
@socketio.on('load_button_config')
def handle_load_button_config():
    from app.utils.M2Service import reload_id
    socketio.emit('execute_ret',{'code':0,'msg':'ok','action':'load_button_config','data':reload_id})

@socketio.on('reload_m2_config')
def handle_reload_m2_config(data):
    result = reload_m2_config_notify(data.get('id'))
    socketio.emit('execute_ret',{'code':0,'msg':'ok','action':'reload_m2_config','data':result})
@socketio.on('gm_diy_pay')
def handle_gm_diy_pay(data):
    c_order_id = secrets.token_hex(16)
    userid =  get_userid_by_character(data.get('charater'))
    if not userid :
        socketio.emit('execute_ret',{'code':-1,'msg':'fail','action':'gm_diy_pay'})
        return
    account = get_account_by_userid(userid)
    serverid = get_server_id_by_userid(userid)
    sdkid = get_sdk_id_by_userid(userid)
    if account:
        diypay(
            server_id=serverid,
            account=account,
            role_id=userid,
            amount=int(data.get('amount')),
            order_id=c_order_id,
            sdk_id=sdkid

        )
        socketio.emit('execute_ret',{'code':0,'msg':'ok','action':'gm_diy_pay'})
    else:
        socketio.emit('execute_ret',{'code':-1,'msg':'fail','action':'gm_diy_pay'})
    
@socketio.on('gm_pay')
def handle_gm_pay(data):
    c_order_id = secrets.token_hex(16)
    userid =  get_userid_by_character(data.get('charater'))
    if not userid :
        socketio.emit('execute_ret',{'code':-1,'msg':'fail','action':'gm_pay'})
        return
    account = get_account_by_userid(userid)
    serverid = get_server_id_by_userid(userid)
    sdkid = get_sdk_id_by_userid(userid)
    if account:
        pay(
            server_id=serverid,
            account=account,
            role_id=userid,
            amount=int(data.get('amount')),
            order_id=c_order_id,
            sdk_id=sdkid

        )
        socketio.emit('execute_ret',{'code':0,'msg':'ok','action':'gm_pay'})
    else:
        socketio.emit('execute_ret',{'code':-1,'msg':'fail','action':'gm_pay'})


# 更新服务器充值配置
@socketio.on('gm_update_recharge_config')
def gm_update_recharge_config(data):
    json_recharge_config: list[dict[str, Any]]= [
        {
            "currency_name":data.get('currency_name'),
            "currency_ratio":data.get('currency_ratio'),   
            "currency_itemid":data.get('currency_itemid'),
            "present_deploy":[],
            "point_deploy":[],
            "present_ratio":"",
            "per_pay_present":[]
        }
    ]
    try:
        update_recharge_config_by_region(region_server_name=data.get('region_server_name'),new_recharge_config = json_recharge_config)
    except Exception as e:
        socketio.emit('execute_ret',{'code':-1,'msg':'update recharge config by region servername fail!','action':'gm_update_recharge_config'})


@socketio.on('gm_get_online_hum_count')
def gm_get_online_hum_count():
    socketio.emit("execute_ret",{'action':'gm_get_online_hum_count','msg':'ok','code':0,'data':{'online':get_online_hum_count()}})

@socketio.on('send_mail')
def handle_send_mail(data):
    userid =  get_userid_by_character(data.get('charater'))
    if not userid :
        socketio.emit('execute_ret',{'code':-1,'msg':'fail','action':'send_mail'})
        return
    item = data.get("item")
    item = data.get("item") if data.get("item") != None and data.get("item") != "" else ""

    
    send_mail(userid,data.get("sender_name"),data.get("lable"),data.get("memo"),item)
    socketio.emit('execute_ret',{'code':0,'msg':'ok','action':'send_mail'})
    return



################################################管理页面############################################





#############################################MirServer####################################################
@bp.route("/gameapi/commodityNotify",methods=["POST"])
def gameapi_commodity_notify():
    req_json = request.form.to_dict()
    CommonUtils.format_json_log(current_app.logger.info,req_json)
    return CommonUtils.json_response(default_ok)

	
@bp.route("/api/GameApi/getGiftList",methods=['POST'])#
def cq_get_gift_list():
    req_json_data = request.form.to_dict()
    CommonUtils.format_json_log(current_app.logger.info,req_json_data)

    return CommonUtils.json_response(
        {
            "code":200,
            "msg":"",
            "time":str(int(datetime.now().timestamp())),
            "data":[
                {"type":1,"reward":"10068#强效太阳水#6"},
                {"type":3,"reward":"10121#强效太阳水(包)#3"},
                {"type":4,"reward":"10121#强效太阳水(包)#5"}
            ],
            "guide":{
                "guide_words":"如何成为盒子会员领取礼包？",
                "guide_img":[
                    {
                        "id":1,
                        "url":"https://static.dhsf.996box.com/box/guideimage/62f37b4ba6619.png",
                        "filename":"62f37b4ba6619.png"
                    },
                    {
                        "id":2,
                        "url":
                        "https://static.dhsf.996box.com/box/guideimage/62f37b4e52e05.png",
                        "filename":"62f37b4e52e05.png"
                    },
                    {
                        "id":3,
                        "url":"https://static.dhsf.996box.com/box/guideimage/62f37b50f0e8d.png",
                        "filename":"62f37b50f0e8d.png"
                    }
                ],
                "guide_step":[
                    {"id":"1","uname":"1、点击下载盒子(www.996box.com)，进入浏览器下载"},
                    {"id":"2","uname":"2、打开并登录996传奇盒子，点击首页会员按钮"},
                    {"id":"3","uname":"3、点击会员页面中的：“立即开通”"}
                ]
            },
            "position":{}
        }
    )

################################################################################################


##############################################Dispatch###########################################


@bp.route("/v1/homeapi/gameindex/EnterGameClient", methods=["GET","POST"])
def enter_game_client():
    with open("data/cq_data/enter_game_client_config.json","r",encoding="utf-8") as fp:
        enter_game_client_config = json.loads(fp.read().replace("{{SDK_BASE_URL}}",DefaultConfig.SDK_BASE_URL))

    json_data = {
        "code": 200,
        "msg": "",
        "time": str(int(datetime.now().timestamp())),
        "data": enter_game_client_config,
        "is_login": 0,
        "is_message": 0
    }
    
    return CommonUtils.json_response(json_data)



@bp.route("/modlist/<path:config_path>",methods=['GET','POST'])
@bp.route("/testmodlist/<path:config_path>",methods=['GET','POST'])

def modlist_v1(config_path: str):
    current_app.logger.info(f"config_path: {config_path}")
    json_data= {
        "code":200,
        "data":[
            f"{DefaultConfig.SDK_BASE_URL}/modlist/v2/modlist.json"#配置url
            ],"msg":"操作成功"} 
    
    return CommonUtils.json_response(json_data)



@bp.route("/modlist/v2/<path:config_path>",methods=['GET','POST'])#二阶段获取服务器配置地址
def modlist_v2(config_path: str):
    current_app.logger.info(f"config_path: {config_path}")
    json_data= {}
    with open("data/cq_data/modlist.json","r",encoding="utf-8") as fp:
        json_data = json.loads(fp.read().replace("{{SDK_BASE_URL}}",DefaultConfig.SDK_BASE_URL))

    for i in range(len(json_data["modData"])):
        
        for j in range(len(json_data["modData"][i]['subMod'])):
            try:
                json_data["modData"][i]['subMod'][j]['operid'] = 1#9762 # 1
            except Exception as e:
                current_app.logger.warnning(f'出现错误: {str(e)}')
    return CommonUtils.json_response(json_data)



@bp.route("/serverlist/<path:config_path>")#三阶段获取服务信息
def server_list(config_path):
    current_app.logger.info(f"config_path: {config_path}")
    json_data= {}
    with open("data/cq_data/serverlist.json","r",encoding="utf-8") as fp:
        json_data = json.loads(fp.read().replace("{{SDK_BASE_URL}}",DefaultConfig.SDK_BASE_URL))
    # encryptedData = dataEncrypt(json.dumps(json_data).encode(encoding='utf-8'),xxtea_sign,xxtea_key)
    # b64_str = base64.b64encode(encryptedData)
    # return Response(b64_str,content_type="text/plain; charset=utf-8")
    return CommonUtils.json_response(json_data)

@bp.route("/notelist/note.json",methods=['GET','POST'])#公告
def note_list():
    with open("data/cq_data/note.json","r",encoding="utf-8") as fp:
        json_data = json.loads(fp.read().replace("{{SDK_BASE_URL}}",DefaultConfig.SDK_BASE_URL))
    return CommonUtils.json_response(json_data)


@bp.route("/api/user/checkHost",methods=['GET'])
def api_user_check_host():
    c_type = request.args.get("type")
    c_host:str = request.args.get("host")

    c_hosts = c_host.split(",")
    json_data = {
        "code":200,
        "msg":"操作成功",
        "ts": int(datetime.now().timestamp()*1000),
        "data":1
    }
    return CommonUtils.json_response(json_data)


##############################################Dispatch###########################################


##############################支付#########################################################################
@bp.route("/api/pay/payTypes",methods=['POST'])
def pay_type():
    json_data = {
        "code": 200,
        "msg": "操作成功",
        "ts": int(datetime.now().timestamp()*1000),
        "data": [
            {
                "main_title": "支付宝",
                "sub_title": "有机会全免",
                "pay_way": 1,
                "folding": 0
            },
            {
                "main_title": "花呗",
                "sub_title": "有机会全免",
                "pay_way": 12,
                "folding": 0
            },
            {
                "main_title": "微信",
                "sub_title": "有机会全免",
                "pay_way": 2,
                "folding": 0
            }
        ]
    }
    return CommonUtils.json_response(json_data)




# {
#     "code": 200,
#     "msg": "操作成功",
#     "ts": 1752136781614,
#     "data": {
#         "order": "alipay_sdk=alipay-sdk-java-dynamicVersionNo&app_id=2019112569400731&biz_content=%7B%22out_trade_no%22%3A%22JAF71016394158973608987402087270%22%2C%22total_amount%22%3A%22648%22%2C%22subject%22%3A%22%E6%B8%B8%E6%88%8F%E5%85%85%E5%80%BC%7C%E8%B0%A8%E9%98%B2%E8%AF%88%E9%AA%97%7C%E6%85%A7%E8%B7%83%EF%BC%88%E4%B8%BAm**oe%E5%85%85%E5%80%BC%EF%BC%89%22%2C%22product_code%22%3A%22QUICK_MSECURITY_PAY%22%2C%22business_params%22%3A%7B%22outTradeRiskInfo%22%3A%22%7B%5C%22mcCreateTradeTime%5C%22%3A%5C%222025-07-10+16%3A39%3A41%5C%22%7D%22%2C%22mc_create_trade_ip%22%3A%22180.117.97.141%22%7D%7D&charset=UTF-8&format=json&method=alipay.trade.app.pay&notify_url=https%3A%2F%2Fpay-sdkv2.dhsf.xqhuyu.com%2Fapi%2Fpay%2Faliapp_callback_hy&sign=POt%2Fk1GgTdnWmTjXgOFkWl2QlZL%2BIKW1SBOiKwhc3mczP2ZTicsr2cdz0nE%2FHuL4SWoaCUSMtesZ6Vsl64hJHe0zpCZrOZpLf4FuDh1zyXUM6jspbvOIijOflGO%2F%2BQ4VhucfJjJpbHbFvMjr0ANp%2Bulgq6nC%2BJoUciWEBiULUyUAS2Lo3ifkXgY%2BtzYnnxELBDAHm5U6t%2BTJJkuUHd41gO8VMb9M6QffUgjQ7YJCm4yyGzwHJocLRq5gqyXjKkhdMMVFoJErrnb9yf758WTD%2B%2FI0yEs3VdEF14eIyv5TeywAmOIRzdG1zSWiwURSs7xsMrQ9%2BBtcsT420i4TX2dpYA%3D%3D&sign_type=RSA2&timestamp=2025-07-10+16%3A39%3A41&version=1.0",
#         "order_no": "JAF71016394158973608987402087270",
#         "status": 1
#     }
# }
@bp.route("/api/pay/orderCreate",methods=['POST'])
@bp.route("/api/pay/orderPlace",methods=['POST'])
def order_place():
    req_json = request.form.to_dict()
    CommonUtils.format_json_log(current_app.logger.info,req_json)
    order_no = CommonUtils.gen_order_no()
    
    biz_cotent  = {
        "out_trade_no": order_no,
        "total_amount": str(req_json.get('price')),
        "subject": "游戏充值|谨防诈骗|慧跃（为m**oe充值）",
        "product_code": "QUICK_MSECURITY_PAY",
        "business_params": {
            "outTradeRiskInfo": json.dumps({"mcCreateTradeTime":datetime.now().strftime("%Y-%m-%d+%H:%M:%S")}) ,
            "mc_create_trade_ip": "0.0.0.0"
        }
    }
    params_json = {
        "alipay_sdk":"alipay-sdk-java-dynamicVersionNo",
        "app_id":2019112569400731,
        "biz_content":json.dumps(biz_cotent),


        "version":"1.0"
    } 
    f_para = CommonUtils.dict_to_params(params_json)
    if req_json.get("pay_way") == '1' or req_json.get("pay_way") == '12':
        
        rsp_json_data = {
            "code":200,
            "msg":"操作成功",
            "ts": int(datetime.now().timestamp()*1000),
            "data":{
                "order": f_para,
                "order_no": order_no,
                "status": 1
            }
        }
    elif req_json.get("pay_way") == '2':
        rsp_json_data = {
            "code":200,
            "msg":"操作成功",
            "ts": int(datetime.now().timestamp()*1000),
            "data":{
                
                "order_no": order_no,
                "mweb_url": f"{DefaultConfig.SDK_BASE_URL}/api/pay/startPay?order_no={order_no}",
                "referer": DefaultConfig.SDK_BASE_URL
            }
        }
    else:
        rsp_json_data = {
            "code":200,
            "msg":"操作成功",
            "ts": int(datetime.now().timestamp()*1000),
            "data":{
                "order":order_no,
                "qr_code":f"{DefaultConfig.SDK_BASE_URL}/api/pay/finishPay?order_no={order_no}".replace("http://","https://"),
                "order_no":order_no,
                "status":1
            }
        }
    order_data[rsp_json_data["data"]["order_no"]] = req_json
    create_qr_code(f"{DefaultConfig.SDK_BASE_URL}/api/pay/finishPay?order_no={order_no}".replace("http://","http://"),f"static/upload/qrcode/{order_no}.jpg")
    return CommonUtils.json_response(rsp_json_data)

def create_qr_code(url, output_file=None, error_correction=qrcode.constants.ERROR_CORRECT_M, 
                   box_size=10, border=4, fill_color="black", back_color="white", 
                   logo_path=None,):
    """
    生成QR码
    
    参数:
    url (str): 需要编码的URL
    output_file (str, optional): 输出文件名。默认为None。
    error_correction (int, optional): 纠错级别。默认为ERROR_CORRECT_M。
    box_size (int, optional): 每个QR码单元的大小。默认为10。
    border (int, optional): QR码边框大小。默认为4。
    fill_color (str, optional): QR码填充颜色。默认为"black"。
    back_color (str, optional): QR码背景颜色。默认为"white"。
    logo_path (str, optional): 要添加到QR码中心的logo图片路径。默认为None。
    """
    # 创建QR码对象
    qr = qrcode.QRCode(
        version=1,
        error_correction=error_correction,
        box_size=box_size,
        border=border,
    )
    
    # 添加数据到QR码
    qr.add_data(url)
    qr.make(fit=True)
    
    # 创建QR码图像
    img = qr.make_image(image_factory=StyledPilImage, fill_color=fill_color, back_color=back_color)
    
    # 如果提供了logo路径，将logo添加到QR码中心
    if logo_path:
        try:
            logo = Image.open(logo_path)
            
            # 计算logo的大小（QR码大小的20%）
            base_width = int(img.size[0] * 0.2)
            wpercent = (base_width / float(logo.size[0]))
            hsize = int((float(logo.size[1]) * float(wpercent)))
            logo = logo.resize((base_width, hsize), Image.Resampling.LANCZOS)
            
            # 计算logo的位置（居中）
            pos = ((img.size[0] - logo.size[0]) // 2, (img.size[1] - logo.size[1]) // 2)
            
            # 将logo粘贴到QR码上
            img.paste(logo, pos)
        except Exception as e:
            logger.info(f"警告: 无法添加logo - {str(e)}")
    
    # 保存QR码图像
    if output_file:
        img.save(output_file)
        logger.info(f"QR码已保存到: {output_file}")

@bp.route("/api/pay/getUserQrcode", methods=['GET'])  # 返回图片PNG二进制数据
def get_user_qrcode():
    order = request.args.get("order")
    order_no = request.args.get("order_no")
    
    if not order_no:
        return Response("Missing 'order_no' parameter", status=400)
    
    try:
        # 安全构建文件路径，避免目录遍历攻击
        # from werkzeug.utils import secure_filename
        # filename = secure_filename()
        filename = f"static/upload/qrcode/{order_no}.jpg"
        with open(filename, "rb") as fp:
            # 自动检测MIME类型
            mimetype, _ = mimetypes.guess_type(filename)
            return Response(fp.read(), mimetype=mimetype)
    except FileNotFoundError:
        return Response("QR code not found", status=404)
    except Exception as e:
        return Response(f"An error occurred: {str(e)}", status=500)
    
@bp.route("/api/pay/startPay", methods=['GET','POST'])
def api_pay_start_pay():
    order = request.args.get("order")
    order_no = request.args.get("order_no")
    
    pay(
        order_id=order_no,
        account=order_data[order_no]["uid"],
        role_id=order_data[order_no]["role_id"],
        amount=order_data[order_no]["price"],
        server_id = order_data[order_no]["server_id"],
        ext_id=2 #元宝
        ) 
    response = make_response(
"""
<!DOCTYPE html>
<html>
<head lang="en">
  <meta http-equiv=Content-Type content="text/html;charset=utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="black">
  <meta name="format-detection" content="telephone=no">
  <title>weixin</title>
  <style>.f10{font-size:10px}.f11{font-size:11px}.f12{font-size:12px}.f13{font-size:13px}.f14{font-size:14px}.f15{font-size:15px}.f16{font-size:16px}.f17{font-size:17px}.f18{font-size:18px}.f19{font-size:19px}.f20{font-size:20px}body{font-size:14px}h1,h2,h3,h4,h5{font-weight:400;font-style:normal}h1,.h1{font-size:20px}h2,.h2{font-size:18px}h3,.h3{font-size:16px}h4,.h4{font-size:14px}h5,.h5{font-size:12px}a,a:visited{color:#007aff}.text_color{color:#888}.title_color{color:#000}.desc{color:#b2b2b2}.warn{color:#b71414}.nickname{color:#576b95}.tips{font-size:13px;color:#b2b2b2}body{background-color:#fff}body.msg_dark{background-color:#2e3132;color:#fff}.page_msg{padding:75px 15px 0;text-align:center}.icon_area{margin-bottom:19px}.text_area{margin-bottom:25px}.text_area .title{margin-bottom:12px}.opr_area{margin-bottom:25px}.extra_area{margin-bottom:20px}@media screen and (min-height:416px){.extra_area{position:fixed;left:0;bottom:0;width:100%}}.btn{display:block;margin-left:auto;margin-right:auto;padding-left:14px;padding-right:14px;font-size:16px;text-align:center;text-decoration:none;overflow:visible;height:40px;border-radius:5px;-moz-border-radius:5px;-webkit-border-radius:5px;box-sizing:border-box;-moz-box-sizing:border-box;-webkit-box-sizing:border-box;color:#fff;line-height:40px;-webkit-tap-highlight-color:rgba(255,255,255,0)}.btn.btn_inline{display:inline-block}.btn_default{background-color:#d1d1d1}.btn_default:not(.btn_disabled):visited{color:#fff}.btn_default:not(.btn_disabled):active{color:rgba(255,255,255,.4);background-color:#a7a7a7}.btn_primary{background-color:#04be02}.btn_primary:not(.btn_disabled):visited{color:#fff}.btn_primary:not(.btn_disabled):active{color:rgba(255,255,255,.4);background-color:#039702}.btn_warn{background-color:#ef4f4f}.btn_warn:not(.btn_disabled):visited{color:#fff}.btn_warn:not(.btn_disabled):active{color:rgba(255,255,255,.4);background-color:#c13e3e}.btn.btn_mini{height:25px;line-height:25px;font-size:14px}button.btn,input.btn{width:100%;border:0;outline:0;-webkit-appearance:none}button.btn:focus,input.btn:focus{outline:0}button.btn_inline,input.btn_inline{width:auto}.btn_disabled{color:rgba(255,255,255,.6)}.btn+.btn{margin-top:10px}.btn.btn_inline+.btn.btn_inline{margin-top:auto;margin-left:10px}.btn_area{margin-left:-5px;margin-right:-5px;font-size:0}.btn_area.btn_area_inline{margin-left:auto;margin-right:auto;display:-webkit-box;display:-webkit-flex;display:-moz-box;display:-ms-flexbox;display:flex}.btn_area.btn_area_inline .btn{margin-top:auto;margin-right:10px;width:100%;-webkit-box-flex:1;-webkit-flex:1;-moz-box-flex:1;-ms-flex:1;box-flex:1;flex:1;display:inline-block \9;width:48% \9;margin-left:1% \9;margin-right:1% \9}.btn_area.btn_area_inline .btn:last-child{margin-right:0}span.btn button{display:block;width:100%;height:100%;background-color:transparent;border:0;outline:0;color:#fff}span.btn button:active{color:rgba(255,255,255,.4)}span.btn.btn_loading button,span.btn.btn_disabled button{color:#fff}.icon_msg{width:100px;height:100px;vertical-align:middle;display:inline-block;border-radius:50%;-moz-border-radius:50%;-webkit-border-radius:50%}.icon_msg.warn{background-color:#f86161;color:#fff;font-size:60px;font-style:normal}html{-ms-text-size-adjust:100%;-webkit-text-size-adjust:100%}body{font:14px/1.5em "Helvetica Neue",Helvetica,Arial,sans-serif;background-color:#efeff4;line-height:1.6}body,h1,h2,h3,h4,h5,p,ul,ol,dl,dd,fieldset,textarea{margin:0}fieldset,legend,textarea,input,button{padding:0}button,input,select,textarea{font-family:inherit;font-size:100%;margin:0;*font-family:"Helvetica Neue",Helvetica,Arial,sans-serif}ul,ol{padding-left:0;list-style-type:none}a img,fieldset{border:0}a{text-decoration:none}</style>
</head>
<body>
  <div class="body">
    <div id="errpage" class="page_msg"></div>
  </div>
  <script type="text/javascript">
    window.onload=function()
    {
        setTimeout(
            function(){
                window.history.back();
            },
            3000
        );
        
    }
  </script>
</body>
</html>
""",200)
    response.headers['X-Organization'] = 'Nintendo'
    return response




@bp.route("/api/pay/finishPay", methods=['GET','POST'])
def api_pay_finish_pay():
    order_no = request.args.get("order_no")
    
    pay(
        order_id=order_no,
        account=order_data[order_no]["uid"],
        role_id=order_data[order_no]["role_id"],
        amount=order_data[order_no]["price"],
        server_id = order_data[order_no]["server_id"],
        ext_id=2 #元宝
        ) 
    
    response = make_response(render_template("pay_finish.html"),200)
    response.headers['X-Organization'] = 'Nintendo'
    return response


@bp.route('/api/pay/postback',methods=['GET','POST'])
def api_pay_postback():
    order_no = request.args.get("order_no")
    pay(
        order_id=order_no,
        account=order_data[order_no]["uid"],
        role_id=order_data[order_no]["role_id"],
        amount=order_data[order_no]["price"],
        server_id = order_data[order_no]["server_id"],
        ext_id=2 #元宝
        ) 
    return CommonUtils.json_response(default_ok)





@bp.route("/mgw.htm",methods=['GET','POST'])
def api_mgw_pay():
   
    msp_param = request.headers['Msp-Param']
    if msp_param != None and msp_param !="":
        msp_param_decoded = urllib.parse.unquote(msp_param)
        msp_param_json = CommonUtils.para_to_dict(msp_param_decoded)
        t = msp_param_json.get('trade_no')
        trade_no_json= json.loads(t)
        CommonUtils.format_json_log(current_app.logger.info,trade_no_json)
        order_no = trade_no_json.get('out_trade_no')
        pay(
            order_id=order_no,
            account=order_data[order_no]["uid"],
            role_id=order_data[order_no]["role_id"],
            amount=order_data[order_no]["price"],
            server_id = order_data[order_no]["server_id"],
            ext_id=2 #元宝
            ) 
        response = make_response(render_template("pay_finish.html"),200)
        response.headers['X-Organization'] = 'Nintendo'
        return response
        
        
    else:
        return b"""00112{"data":{"api_name":"com.alipay.mcpay","api_version":"4.9.0","code":"0","namespace":"com.alipay.mobilecashier"}}00432"""
##############################支付#########################################################################



#################################################################################################################




@bp.route("/logstores/client_log/track",methods=['GET','POST'])
def track():
    CommonUtils.json_response(default_ok)

@bp.route("/v1/newLog",methods=['POST'])
def new_log():
    CommonUtils.format_json_log(current_app.logger.info,json.loads(request.data))
    return CommonUtils.json_response({"code":200})




@bp.route("/gameapi/chargeState",methods=['GET','POST'])
def charge_state():
    json_data = {"code":200,"data":{"status":1},"msg":"请求成功"}
    return CommonUtils.json_response(json_data)

@bp.route("/api/user/cheatDetection/checkRiskV6",methods=['GET','POST'])
def api_user_cheatDetection_checkRiskV6():
    json_data = {
        "code": 200,
        "msg": "操作成功",
        "ts": int(datetime.now().timestamp()*1000),
        "data": []
    }
    return CommonUtils.json_response(json_data)

@bp.route("/game/game-server/v1/sendPropResourceToGame",methods=['GET'])#
def cq_send_prop_resource_to_game():
    CommonUtils.format_json_log(current_app.logger.info,request.args.to_dict())
    return CommonUtils.json_response({"code":200,"msg":"操作成功","data": True,"success":True})

#################################################################################################################


##############################################传奇#############################################


@bp.route("/box_serverlist/box_server_list.json", methods=["GET","POST"])
def box_server_list():
    with open("data/cq_data/box_server_list.json","r",encoding="utf-8") as fp:
        json_data = json.loads(fp.read())
    return CommonUtils.json_response(json_data)



@bp.route("/v1/homeapi/gameindex/myGames",methods=['GET','POST'])
def my_games():
    json_data= {
        "code": 200,
        "msg": "",
        "time": str(int(datetime.now().timestamp())),
        "data": {
            "game_list": [
                {
                    "box_game_id": 9762,
                    "game_logo_url": "https://static.dhsf.996box.com/box/logo/9762/658934efd28e4.png",
                    "game_name": "传奇开发",
                    "game_tags": "三职业",
                    "game_version_name": "1.76",
                    "game_appid": 1,
                    "game_time": 0,
                    "oper_name": "stcq_9762",
                    "ios_download_url": "",
                    "download_pc": 1,
                    "download_ad": 1,
                    "download_ios": 1,
                    "game_type": 1,
                    "cs_run_in_box": 0,
                    "pc_game_type": 1,
                    "no_need_download": 0
                }
                
            ]
        },
        "is_login": 0,
        "is_message": 0
    }
    

    return CommonUtils.json_response(json_data)




@bp.route("/loginClient/version_login.txt",methods=['GET','POST'])
def version_login():
    json_data= {"version":"1.3.0"}    
    return CommonUtils.json_response(json_data)




@bp.route("/client_tool_example_cq/version_996M2_debug.txt",methods=['GET','POST'])
def version_996M2_debug():
    json_data= {"version":"1.3.4"}    

    return CommonUtils.json_response(json_data)



##############################交易行相关#######################################




@bp.route("/gameapi/getEquipType",methods=['GET','POST'])
def get_equip_type():
    json_data = {
        "code":200,
            "data": {
                "list":{
                    "1":"衣服",
                    "2":"武器",
                    "3":"特殊装备",
                    "4":"首饰",
                    "5":"时装",
                    "6":"专属首饰",
                    "7":"其他"
                },
                "sell_desc":"购买后的装备会直接发放至邮件，1小时内不可在交易行中出售",
                "sell_config":{
                    "role_sell_switch":1,
                    "coin_sell_switch":0,
                    "equip_sell_switch":0
                }
            },
            "msg":"请求成功"
        }
    return CommonUtils.json_response(json_data)


@bp.route("/gameapi/commodityList",methods=['GET','POST'])
def commpdity_list():
    type_id = request.json['type']
    page_num = request.json['pagenum']
    page = request.json['page']


    json_data = {
        "code":200,
        "data":{
            "total":1,
            "per_page":10,
            "current_page":1,
            "last_page":1,
            "data":[
                {
                    "type":1,
                    "id":37933864,
                    "role_level":37,
                    "role":"兔兔兔",
                    "price":"20.00",
                    "role_config_id":"1",
                    "coin_config_type_name":"",
                    "coin_config_id":0,
                    "target":0,
                    "role_id":"83394950001739961998000018958",
                    "target_roleid":"",
                    "vip":1,
                    "status":1,
                    "sex":0,
                    "coin_num":0,
                    "equip_type_id":None,
                    "title":"兔兔兔",
                    "bargain_switch":1,
                    "status_ch":"已上架",
                    "type_ch":"角色",
                    "equip_type_ch":"其他",
                    "equip_id":"",
                    "equip_num":1
                },
                {
                    "type":1,
                    "id":37933868,
                    "role_level":145,
                    "role":"罗小黑",
                    "price":"325.00",
                    "role_config_id":"2",
                    "coin_config_type_name":"",
                    "coin_config_id":0,
                    "target":0,
                    "role_id":"83394950001739961998000018432",
                    "target_roleid":"",
                    "vip":1,
                    "status":1,
                    "sex":1,
                    "coin_num":32658998,
                    "equip_type_id":None,
                    "title":"罗小黑",
                    "bargain_switch":1,
                    "status_ch":"已上架",
                    "type_ch":"角色",
                    "equip_type_ch":"其他",
                    "equip_id":"",
                    "equip_num":1
                },
                
                {
                    "type":1,
                    "id":37933868,
                    "role_level":81,
                    "role":"超牛",
                    "price":"120.00",
                    "role_config_id":"0",
                    "coin_config_type_name":"",
                    "coin_config_id":0,
                    "target":0,
                    "role_id":"83394950001739961998000013258",
                    "target_roleid":"",
                    "vip":1,
                    "status":1,
                    "sex":0,
                    "coin_num":35882,
                    "equip_type_id":None,
                    "title":"超牛",
                    "bargain_switch":1,
                    "status_ch":"已上架",
                    "type_ch":"角色",
                    "equip_type_ch":"其他",
                    "equip_id":"",
                    "equip_num":1
                }
            ]
        },
        "msg":"请求成功"
    }
    return CommonUtils.json_response(json_data)


@bp.route('/gameapi/targetCommodity',methods=['GET','POST'])
def target_commodity():
    # type_id = request.json['type']
    page_num = request.json['pagenum']
    page = request.json['page']
    json_data = {
        "code":200,
        "data":{
            "total":0,
            "per_page":10,
            "current_page":1,
            "last_page":0,
            "data":[]
        },
        "msg":"请求成功"
    }
    return CommonUtils.json_response(json_data)





@bp.route('/gameapi/sellConfig',methods=['GET','POST'])
def shell_config():
    json_data = {
        'code':200,
        'msg':'操作成功',
        'data':None
    }
    return CommonUtils.json_response(json_data)
##############################交易行相关##########################################


@bp.route('/api/user/checkHost',methods=['GET','POST'])
def checkHost():
    json_data = {
        "code": 200,
        "msg": "操作成功",
        "ts": int(datetime.now().timestamp()),
        "data": 1
    }
    return CommonUtils.json_response(json_data)


@bp.route("/cq/api",methods=['POST'])#一阶段更新客户端env.json
def cq_api():
    json_data = json.loads(request.data)
    # CommonUtils.format_json_log(current_app.logger.info,json_data)
    if json_data.get("type") == "log_upload":
        socketio.emit('log_content_update',{"content":json_data.get('log_content')})
    return CommonUtils.json_response({"code":200,"msg":"操作成功","data": True,"success":True})


@bp.route("/svip/game/v1/querySvipBaseGameRight/",methods=['GET'])#
def cq_query_svip_base_game_right():
    return CommonUtils.json_response(
        {
            "code":200,
            "msg":"操作成功",
            "data":{
                "levelNum":8,
                "rights":[]
            },
            "success":True
        }
    )





@bp.route("/api/GameApi/sendGift",methods=['GET','POST'])
def send_gift():
    gift_type = 1
    return CommonUtils.json_response(
        {"code":200,"msg":"","time":{str(int(datetime.now().timestamp()))},"data":{"type":gift_type}}
    )



######################################################版本上传 ############################################################



@bp.route('/api/cq/upload', methods=['POST'])
def api_cq_upload():
    # 检查请求中是否包含文件
    if 'file' not in request.files:
        return {'error': '未找到文件'}, 400
    element_name = ""
    file = request.files['file']

    # 检查文件名是否有效
    if file.filename == '':
        return {'error': '无效的文件名'}, 400

    # 获取当前日期
    now = datetime.now()
    year = str(now.year)
    month = str(now.month).zfill(2)
    day = str(now.day).zfill(2)

    # 创建存储路径
    base_dir = os.path.join('data/cq_data/package')
    os.makedirs(base_dir, exist_ok=True)

    # 生成随机文件名
    random_hex = secrets.token_hex(32)
    f_name, f_ext = os.path.splitext(file.filename)
    _type = "text"
    
    if "zip" in f_ext.lower() :
        _type = "zip"

    else:
        
        return Response(get_response_string(-1),status=200,content_type="application/json")
        


    new_filename = file.filename

    # 构建完整文件路径
    file_path = os.path.join(base_dir, new_filename).replace(r'\\','/')


    try:
        if os.path.exists(file_path):
            os.remove(file_path)
        if os.path.exists(os.path.join(base_dir,'hotupdate')):
            shutil.rmtree(os.path.join(base_dir,'hotupdate'))
        
        # 保存文件
        file.save(file_path)
        file_path_v2 ="/"+ file_path
        # with open('data/cq_data/version_upload.json','w',encoding='utf-8') as fp:
        #     data_str = fp.read()
        #     if data_str == '':
        #         data_str = '{}'
        #     json_data =  json.loads(data_str)
    
        CommonUtils.unzip_file(file_path, base_dir)
        return Response(get_response_string(0),status=200,content_type="application/json")
    except Exception as e:
        return Response(get_response_string(-1),status=200,content_type="application/json")
    

@bp.route('/view/cq_version_upload', methods=['GET'])
def cq_version_upload():
    response = make_response(render_template("cq_version_upload.html"),200)
    response.headers['X-Organization'] = 'Nintendo'
    return response



@bp.route('/coustom/<path:path>')
def redirect_static(path):
    refer = path.split('/')[0]
    file =  path.split('/')[1]
    
    return send_from_directory('data/cq_data/package', file)


