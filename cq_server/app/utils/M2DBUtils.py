from decimal import Decimal
from datetime import datetime
import json
import traceback
from typing import Any
from app.utils.LoggerManager import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from app.sql_class.Legend import TBLBOXSELL, TBLCHARACTER, Pay,Diypay,TBLMAIL,t_TBL_CONFIG
from app.settings import DefaultConfig
from app.utils.M2Service import mail_notify

# 创建连接
engine = create_engine(DefaultConfig.M2_DATABASE)
# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session: Session = SessionLocal()


######################

def send_mail(role_id:str,sender_name:str,lable:str,memo:str,item:str=''):
    if isinstance(item,dict) or isinstance(item,list):
        item = json.dumps(item,ensure_ascii=False)

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

    


def get_userid_by_character(character: str) -> str | None:
    try:
        result = session.query(TBLCHARACTER.FLD_USERID) \
            .filter(TBLCHARACTER.FLD_CHARACTER == character) \
            .first()
        session.close()
        return result[0] if result else None
    except Exception as e:
        session.close()
        return None
     
def get_account_by_userid(user_id: str) -> str | None:
    """通过用户ID从 TBL_CHARACTER 表中查询 FLD_ACCOUNT"""
    try:
        result = session.query(TBLCHARACTER.FLD_ACCOUNT) \
            .filter(TBLCHARACTER.FLD_USERID == user_id) \
            .first()
        session.close()
        return result[0] if result else None
    except :
        session.close()
        return None
def get_user_level_by_userid(user_id: str) ->str|int|None:
    try:
        result = session.query(TBLCHARACTER.FLD_LEVEL) \
            .filter(TBLCHARACTER.FLD_USERID == user_id) \
            .first()
        session.close()
        return result[0] if result else None
    except :
        session.close()
        return None

def get_jobid_by_userid(user_id:str):
    try:
        result = session.query(TBLCHARACTER.FLD_JOB) \
            .filter(TBLCHARACTER.FLD_USERID == user_id) \
            .first()
        session.close()
        return result[0] if result else None
    except :
        session.close()
        return None
def get_jobname_by_jobid(jobid:int):
    job_data = ["战士","法师","道士"]
    return job_data[jobid]
    
def get_server_id_by_userid(user_id: str) -> str | None:
    """通过用户ID从 TBL_CHARACTER 表中查询 FLD_SERVERID"""
    try:
        result = session.query(TBLCHARACTER.FLD_SERVERID) \
            .filter(TBLCHARACTER.FLD_USERID == user_id) \
            .first()
        session.close()
        return result[0] if result else None
    except :
        session.close()
        return None
    
def get_sdk_id_by_userid(user_id: str) -> str | None:
    """通过用户ID从 TBL_CHARACTER 表中查询 FLD_SDKID"""
    try:
        result = session.query(TBLCHARACTER.FLD_SDKID) \
            .filter(TBLCHARACTER.FLD_USERID == user_id) \
            .first()
        session.close()
        return result[0] if result else None
    except :
        session.close()
        return None

def get_recharge_config_by_tblconfig():
    try:
        result = session.query(t_TBL_CONFIG.c.recharge_config).first()
        session.close()
        return result[0] if result else None
        
    except Exception as e:
        session.close()
        logger.error(str(e))
        logger.error(traceback.format_exc())

        return """{"currency_name":"元宝","currency_ratio":10,"currency_itemid":2,"present_deploy":[],"point_deploy":[],"present_ratio":"","per_pay_present":[]}"""
def get_server_name():
    try:
        result = session.query(t_TBL_CONFIG.sRegionServerName).first()
        return result[0] if result else None
    except:
        session.close()
        return None

# 2. 按 sRegionServerName 更新 recharge_config 的函数
def update_recharge_config_by_region(region_server_name: str, new_recharge_config: list[dict[str, Any]]):
    """
    根据服务器名称更新充值配置
    :param region_name: 目标服务器名称（对应 sRegionServerName 字段）
    :param new_recharge_config: 新的充值配置（字符串格式，建议 JSON 串）
    :return: 是否更新成功
    """
    try:
        # 定位目标记录：按 sRegionServerName 精确匹配
        target_config = session.query(t_TBL_CONFIG).filter(
            t_TBL_CONFIG.sRegionServerName == region_server_name
        ).first()

        if not target_config:
            logger.info(f"错误：未找到服务器名称为「{region_server_name}」的配置记录")
            return False

        # 更新 recharge_config 字段
        target_config.recharge_config = new_recharge_config
        # 可选：更新最后修改时间（若表中有对应字段，如 AddTime/UpdateTime）
        # target_config.UpdateTime = datetime.now()

        session.commit()  # 提交修改
        session.refresh(target_config)  # 刷新实例，获取最新数据
        logger.info(f"成功：服务器「{region_server_name}」的充值配置已更新")
        return True

    except Exception as e:
        session.rollback()  # 出错回滚，避免数据不一致
        logger.info(f"失败：更新充值配置时出错 - {str(e)}")
        return False

    finally:
        session.close()  # 无论成功与否，关闭会话

def add_tbl_config(region_server_name: str):
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


def fix_pre_order(order):
    result = session.query(Pay) \
                .filter(Pay.sGameOrder == order) \
                .first()
    if not result:
        return
    result.DrawOut = 0
    session.commit()

def fix_pre_diy_order(order):
    result = session.query(Diypay) \
                .filter(Diypay.sGameOrder == order) \
                .first()
    if not result:
        return
    result.DrawOut = 0
    session.commit()

#######################



def add_pay(server_id:str,account:str,role_id:str,amount:int,order_id:str,pay_id:str,sdk_id:int=1,draw_out:int = 0,ext_data:str=2,product_id:str="0",ext_id:int=2):
    session: Session = SessionLocal()
    try:
   
        new_pay: Pay = Pay(
            PayId=pay_id,
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
        return
    
    except Exception as e:
        session.rollback()
        # logger.info(f"插入失败: {str(e)}")
    finally:
        session.close()
    return


def add_diypay(server_id:str,account:str,role_id:str,amount:int,order_id:str,pay_id:str,sdk_id:int=1,draw_out:int = 0,ext_data:str=2,product_id:str="0",ext_id:int=2):
    session: Session = SessionLocal()
    try:
   
        new_diypay : Diypay= Diypay(
            PayId=pay_id,
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

    except Exception as e:
        session.rollback()
        # logger.info(f"插入失败: {str(e)}")
    finally:
        session.close()



