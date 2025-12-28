
import json
import socket

from app.settings import DefaultConfig
reload_id = {
    1:"重载物品表",
    2:"重载怪物表",
    3:"重载怪物爆率表",
    4:"重载Game_Data表",
    5:"重载商城配置",
    7:"重载QF",
    8:"重载QM",
    15:"重载Robot",
    17:"重载!Setup.txt",
    18:"重载机器人专用脚本",
    19:"重载沙巴克配置",       
    20:"重载套装数据库",
    21:"重载LuaFunc",
    22:"重载LuaCond",
    30:"重载Buff数据",
    99:"重载所有NPC"
}
def send_tcp_data(data,address = DefaultConfig.M2_SERVICE_ADDRESS):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(address)
    
    try:
        client_socket.send(data)
        data = client_socket.recv(1024)
        return data
    except Exception as e:
        pass

def reload_gift_list():
    #重载礼包
    rsp = send_tcp_data(data = json.dumps({"msgid":2017},ensure_ascii=False).encode("gb2312"))
    return rsp.decode("gb2312")

def get_online_hum_count():
    #在线人数
    rsp = send_tcp_data(data = json.dumps({"msgid":2008},ensure_ascii=False).encode("gb2312"))
    return rsp.decode("gb2312")

def send_pay_notify(userid:str,roleid:str):
    #支付通知
    rsp = send_tcp_data(data = json.dumps({"msgid":2001,"roleid":roleid,"userid":userid},ensure_ascii=False).encode("gb2312"))
    return rsp.decode("gb2312")


def send_diy_pay_notify(roleid:str):
    rsp = send_tcp_data(data = json.dumps({"msgid":2020,"roleid":roleid},ensure_ascii=False).encode("gb2312"))
    return rsp.decode("gb2312")



# def recharge_config_state():
#     rsp = send_tcp_data(data = json.dumps({"msgid":2005},ensure_ascii=False).encode("gb2312"))
#     return rsp.decode("gb2312")
# def recharge_config():
#     rsp = send_tcp_data(data = json.dumps({"msgid":2006},ensure_ascii=False).encode("gb2312"))
#     return rsp.decode("gb2312")
    
def tongqu_reboot():
    #通区重启
    rsp = send_tcp_data(data = json.dumps({"msgid":2018},ensure_ascii=False).encode("gb2312"))
    return rsp.decode("gb2312")

#寄售角色
def sell_chrarcter_notify(s_user_account:str,s_user_id:str,s_order:str,s_http_url:str):
    
    rsp = send_tcp_data(data = json.dumps({"msgid":2016,"sUserAccount":s_user_account,"sUserID":s_user_id,"sOrder":s_order,"sHttpUrl":s_http_url},ensure_ascii=False).encode("gb2312"))
    return rsp.decode("gb2312")


# 购买角色请求
def buy_chrarcter_a_notify(s_buy_account:str,s_shell_account:str,s_shell_user_id:str,s_order:str,s_http_url:str,serverid:str,updatetype:str=1,pay_order:str=0,password:str=""):
    rsp = send_tcp_data(data = json.dumps({"msgid":2011,"sBuyAccount":s_buy_account,"sSellAccount":s_shell_account,"sSellUserID":s_shell_user_id,"sOrder":s_order,"upDateType":"1","payOrder":"0","serverid":"9306444","password":password,"sHttpUrl":s_http_url},ensure_ascii=False).encode("gb2312"))
    return rsp.decode("gb2312")

# 确认角色购买
def buy_chrarcter_b_notify(s_user_account:str,s_user_id:str,s_order:str,s_http_url:str):
    
    rsp = send_tcp_data(data = json.dumps({"msgid":2010,"sUserAccount":s_user_account,"sUserID":s_user_id,"sOrder":s_order,"sHttpUrl":s_http_url},ensure_ascii=False).encode("gb2312"))
    return rsp.decode("gb2312")



#服务器维护
def service_off_notify():
    rsp = send_tcp_data(data = json.dumps({"msgid":2003,"command":"service_off"}).encode("gb2312"))
    return rsp.decode("gb2312")

def online_time_notify(rolename:str):
    rsp = send_tcp_data(data = json.dumps({"rolename":rolename,"msgid":2003,"command":"onlinetime"},ensure_ascii=False).encode("gb2312"))
    return rsp.decode("gb2312")

def playerlv_notify(rolename:str):
    rsp = send_tcp_data(data = json.dumps({"rolename":rolename,"msgid":2003,"command":"playerlv"},ensure_ascii=False).encode("gb2312"))
    return rsp.decode("gb2312")

def reload_m2_config_notify(id:int):
    rsp = send_tcp_data(data = json.dumps({"msgid":"2003","command":"reloadxls","id":str(id)},ensure_ascii=False).encode("gb2312"))
    return rsp.decode("gb2312")
    

#发送公告
def send_notify_notify(text:str,begin_time:int,type:int=1,color:int=249,interval_time:int=60,line_time:int=240):
    rsp = send_tcp_data(data = json.dumps({"begin_time":begin_time,"color":color,"interval_time":interval_time,"line_time":line_time,"msgid":2005,"ny":0,"text":text,"type":type},ensure_ascii=False).encode("gb2312"))
    return rsp.decode("gb2312")
    
#新邮件通知
def mail_notify(rolename:str):
    rsp = send_tcp_data(data = json.dumps({"rolename":rolename,"msgid":2003,"command":"mail_notify"},ensure_ascii=False).encode("gb2312"))
    return rsp.decode("gb2312")


def query_money_notify(rolename:str,id:int):
    rsp = send_tcp_data(data = json.dumps({"rolename":rolename,"msgid":2003,"command":"money_query","id":id},ensure_ascii=False).encode("gb2312"))
    return rsp.decode("gb2312")

def account_info_notify(rolename:str,roleaccount:str):
    rsp = send_tcp_data(data = json.dumps({"msgid":2036,"rolename":rolename,"roleaccount":roleaccount},ensure_ascii=False).encode("gb2312"))
    return rsp.decode("gb2312")
    
def account_login_disable_notify(account:str,note:str,time_sec:int):
    rsp = send_tcp_data(data = json.dumps({"account":account,"command":"login_disable","msgid":2003,"note":note,"time":time_sec},ensure_ascii=False).encode("gb2312"))
    return rsp.decode("gb2312")
    

def account_enable_login_notify(account):
    rsp = send_tcp_data(data = json.dumps({"account":account,"command":"login_enable","msgid":2003} ,ensure_ascii=False).encode("gb2312"))
    return rsp.decode("gb2312")
    
def reload_config_notify():
    rsp = send_tcp_data(data = json.dumps({"msgid":2033} ,ensure_ascii=False).encode("gb2312"))
    return rsp.decode("gb2312")
    
def load_recharge_config_notify():
    rsp = send_tcp_data(data = json.dumps({"msgid":2006},ensure_ascii=False).encode("gb2312"))
    return rsp.decode("gb2312")




# 使用示例
if __name__ == "__main__":
    
    print("\n\n\n\n\n")

    # print(send_notify_notify("公告:服务器即将更新! 请注意保存数据!",int(datetime.now().timestamp())))
    # print(service_off_notify) 

    # for i in range(99):
    #     print(reload_m2_config_notify(i))
    #     time.sleep(0.25)

    # for v in reload_id:
    #     print(reload_id[v])
    #     print(reload_m2_config_notify(v))
    #     time.sleep(0.25)


    #寄售角色
    s_http_url = "http://charge-api.996box.com/gameapi/commodityNotify"
    print(sell_chrarcter_notify("2019826772","93064440001751569323000189563","00000002",s_http_url))
    #买下角色步骤一
    print(buy_chrarcter_a_notify("2019826772","2019826772","93064440001751569323000189563","00000002",s_http_url,"9306444"))
    #买下角色步骤二  
    print(buy_chrarcter_b_notify("2019826772","93064440001751569323000189563","00000002",s_http_url))
    pass