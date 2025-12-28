import threading

from jinja2 import Environment, FileSystemLoader
import requests
from app.utils.CommonUtils import *

from app.settings import DefaultConfig
from gameservice.lua_engine import LuaEngine
def init():
    global private_pem,public_pem
    private_pem,public_pem = CommonUtils.create_rsa_key()
    global public_key,private_key
    private_key = CommonUtils.load_private_key(private_pem)
    public_key = CommonUtils.load_public_key(public_pem)
def rsa_test():
    
    init()

    text = "08u873894hjkghfisdghyuifg你好~！@#￥%……&*（——++"
    encrypted_bytes = CommonUtils.rsa_encrypt_chunks(text.encode(),public_key)
    encrypted_text = base64.b64encode(encrypted_bytes).decode()
    print(f"加密:{text}\n 密文:{encrypted_text}")
    encrypted_bytes = base64.b64decode(encrypted_text)
    private_key = CommonUtils.load_private_key(private_pem)
    decrypted_bytes = CommonUtils.rsa_decrypt_chunks(encrypted_bytes,private_key)
    print(f"解密后:{decrypted_bytes.decode()}")


def password_to_hash_test():
    
    pwd = "N2505G1025U51I10P0"
    hashed_password = CommonUtils.password_to_hash(pwd)
    print(f"对 {pwd} 进行hash后的结果为:")
    print(hashed_password)
    print(f"对 {pwd} 进行hash校验结果为:")
    check_status = CommonUtils.verify_password(pwd,hashed_password)
    if(check_status):
        print("验证成功")
    else:
        print("验证失败")
    print("模拟错误的密码验证")
    check_status = CommonUtils.verify_password("474+54657+865346874684684654564！@#￥%……&*（）（——）",hashed_password)
    if(check_status):
        print("验证成功")
    else:
        print("验证失败")
def rsa_sign_test():
    

    print("sha256 + rsa 签名验证")
    p = "a=13&uid=15&uuid=&k=0"
    para_dict = CommonUtils.para_to_dict(p,False)
    print(para_dict)
    sorted = CommonUtils.sort_para_to_str(para_dict)
    signed_data = CommonUtils.rsa_sign(private_key,sorted.encode())
    signed_data_b64 = base64.b64encode(signed_data).decode()
    print(signed_data_b64)
    signed_data = base64.b64decode(signed_data_b64) 
    rsa_verify_result = CommonUtils.rsa_verify(public_key,sorted.encode(),signed_data)
    if rsa_verify_result:
        print("验证成功")
    else:
        print("验证失败")

def register_test():
    import requests

    rsp = requests.post("http://127.0.0.1/api/send_mail_captcha",json={"email":"admin@outlook.com"})
    print(rsp.json())
    ticket = rsp.headers["X-Ticket"]

    verify_code = input("请输入验证码:")
    rsp = requests.post("http://127.0.0.1/api/register",headers={"X-Ticket":ticket},json={"is_encrypt":"false","verify_code":verify_code,"account":"admin","phone_number":"17398523365","username":"涩涩大魔王","avatar_url":"","password":"admin"})
    print(rsp.json())
    pass

def send_email_test():
    # 创建 Jinja2 环境
    env = Environment(loader=FileSystemLoader('.'))
    # 加载模板文件
    template = env.get_template('templates/verify_code.html')
    # 定义要替换的变量
    data = {
        'verify_url': 'https://example.com/verify',
        'verify_code': '123456'
    }

    # 渲染模板
    output = template.render(data)

    CommonUtils.send_mail(
        smtp_server='smtp.126.com',
        port=25,
        username='admin@126.com',
        password='admin39887454iu',
        sender='admin@126.com',
        receiver="admin@outlook.com",
        subject='这是你的验证码',
        body=output,type='html')
# def parse_encrypt_resume():
#     import yaml
#     from proto.resume_pb2 import Resume,PersonalInfo,Education,ProjectWork,SkillsIntroduction,TagList,WorkExperience
#     from app.utils.Ec2b import Ec2b
#        # 打开并加载 YAML 文件
#     with open(os.path.join(DefaultConfig.BASE_DIR, "data/resume_default.yaml"), mode="r", encoding='utf-8') as fp:
#         resume_yaml = yaml.safe_load(fp)

#     # 创建 Resume 消息对象
#     resume_proto = Resume()

#     # 处理个人信息
#     person_info_yaml = resume_yaml.get('person_info', {})
#     person_info_proto = PersonalInfo()
#     person_info_proto.birth = person_info_yaml.get('birth', '')
#     person_info_proto.school = person_info_yaml.get('school', '')
#     person_info_proto.education = person_info_yaml.get('education', '')
#     person_info_proto.major = person_info_yaml.get('major', '')
#     person_info_proto.native_place = person_info_yaml.get('native_place', '')
#     person_info_proto.current_place = person_info_yaml.get('current_place', '')
#     person_info_proto.email = person_info_yaml.get('email', '')
#     person_info_proto.phone = person_info_yaml.get('phone', '')
#     person_info_proto.address = person_info_yaml.get('address', '')
#     person_info_proto.content = person_info_yaml.get('content', '')
#     person_info_proto.label = person_info_yaml.get('label', '')
#     person_info_proto.name = person_info_yaml.get('name', '')
#     person_info_proto.photo_url = person_info_yaml.get('photo_url', '')
#     resume_proto.personal_info.CopyFrom(person_info_proto)

#     # 处理教育经历
#     educations_yaml = resume_yaml.get('education', [])
#     for edu_yaml in educations_yaml:
#         edu_proto = Education()
#         edu_proto.degree = edu_yaml.get('degree', '')
#         edu_proto.major = edu_yaml.get('major', '')
#         edu_proto.school_name = edu_yaml.get('school_name', '')
#         edu_proto.time = edu_yaml.get('time', '')
#         resume_proto.educations.append(edu_proto)

#     # 处理项目作品
#     project_works_yaml = resume_yaml.get('project_works', [])
#     for project_yaml in project_works_yaml:
#         project_proto = ProjectWork()
#         project_proto.name = project_yaml.get('name', '')
#         project_proto.work_time = project_yaml.get('work_time', '')
#         project_proto.content = project_yaml.get('content', '')
#         resume_proto.project_works.append(project_proto)

#     # 处理技能概述
#     skills_yaml = resume_yaml.get('skills_introduction', {})
#     skills_proto = SkillsIntroduction()
#     skills_proto.title = skills_yaml.get('title', '')
#     skills_proto.content = skills_yaml.get('content', '')
#     resume_proto.skills_introduction.CopyFrom(skills_proto)

#     # 处理标签列表
#     tag_lists_yaml = resume_yaml.get('tag_list', [])
#     for tag_yaml in tag_lists_yaml:
#         tag_proto = TagList()
#         tag_proto.icon = tag_yaml.get('icon', '')
#         tag_proto.name = tag_yaml.get('name', '')
#         resume_proto.tag_lists.append(tag_proto)

#     # 处理工作经历
#     work_experiences_yaml = resume_yaml.get('work_experience', [])
#     for work_yaml in work_experiences_yaml:
#         work_proto = WorkExperience()
#         work_proto.company_name = work_yaml.get('company_name', '')
#         work_proto.position = work_yaml.get('position', '')
#         work_proto.work_time = work_yaml.get('work_time', '')
#         work_proto.work_content = work_yaml.get('work_content', '')
#         resume_proto.work_experiences.append(work_proto)

#     # 序列化 Resume 消息对象为字节
#     serialized_bytes = resume_proto.SerializeToString()
#     with open(DefaultConfig.CLIENT_SECRET_KEY_FILE,"rb") as fp:
#         csk = fp.read()
#     key,data = Ec2b.LoadKey(csk)
#     seed = Ec2b.GetSeed(key,data)
#     temp =  Ec2b.SetSeed(seed)

#     encrypted_bytes = Ec2b.Xor(serialized_bytes,temp)
#     with open("data/resume.dat","wb") as fp:
#         fp.write(encrypted_bytes)


# def parse_encrypted_resume():
#     import yaml
#     from proto.resume_pb2 import Resume
#     from app.utils.Ec2b import Ec2b
#     from app.settings import DefaultConfig

#     # 1. 读取加密文件
#     with open("data/resume.dat", "rb") as fp:
#         encrypted_bytes = fp.read()

#     # 2. 生成解密所需的种子
#     with open(DefaultConfig.CLIENT_SECRET_KEY_FILE, "rb") as fp:
#         csk = fp.read()
#     key, data = Ec2b.LoadKey(csk)
#     seed = Ec2b.GetSeed(key, data)
#     temp = Ec2b.SetSeed(seed)

#     # 3. 解密数据
#     decrypted_bytes = Ec2b.Xor(encrypted_bytes, temp)

#     # 4. 解析 Protobuf 字节
#     resume_proto = Resume()
#     resume_proto.ParseFromString(decrypted_bytes)

#     # 5. 转换为字典结构
#     resume_dict = {
#         "person_info": {
#             "birth": resume_proto.personal_info.birth,
#             "school": resume_proto.personal_info.school,
#             "education": resume_proto.personal_info.education,
#             "major": resume_proto.personal_info.major,
#             "native_place": resume_proto.personal_info.native_place,
#             "current_place": resume_proto.personal_info.current_place,
#             "email": resume_proto.personal_info.email,
#             "phone": resume_proto.personal_info.phone,
#             "address": resume_proto.personal_info.address,
#             "content": resume_proto.personal_info.content,
#             "label": resume_proto.personal_info.label,
#             "name": resume_proto.personal_info.name,
#             "photo_url": resume_proto.personal_info.photo_url
#         },
#         "education": [
#             {
#                 "degree": edu.degree,
#                 "major": edu.major,
#                 "school_name": edu.school_name,
#                 "time": edu.time
#             } for edu in resume_proto.educations
#         ],
#         "project_works": [
#             {
#                 "name": proj.name,
#                 "work_time": proj.work_time,
#                 "content": proj.content
#             } for proj in resume_proto.project_works
#         ],
#         "skills_introduction": {
#             "title": resume_proto.skills_introduction.title,
#             "content": resume_proto.skills_introduction.content
#         },
#         "tag_list": [
#             {
#                 "icon": tag.icon,
#                 "name": tag.name
#             } for tag in resume_proto.tag_lists
#         ],
#         "work_experience": [
#             {
#                 "company_name": exp.company_name,
#                 "position": exp.position,
#                 "work_time": exp.work_time,
#                 "work_content": exp.work_content
#             } for exp in resume_proto.work_experiences
#         ]
#     }


#     return resume_dict
    
import hashlib

# 假设参与签名计算的原始数据是 domain、serverid 拼接后的字符串
# 这里 domain 为空字符串，实际情况中应根据具体业务确定


# 假设使用 MD5 算法进行签名（实际算法需根据真实情况确定）
def calculate_md5_sign(data):
    md5 = hashlib.md5()
    md5.update(data.encode('utf-8'))
    return md5.hexdigest()

# 假设使用 SHA256 算法进行签名（实际算法需根据真实情况确定）
def calculate_sha256_sign(data):
    sha256 = hashlib.sha256()
    sha256.update(data.encode('utf-8'))
    return sha256.hexdigest()
    




def main():

    # rsa_test()
    # rsa_sign_test()
    # password_to_hash_test()
    # register_test()
    # send_email_test()
    # print(os.path.join(DefaultConfig.BASE_DIR,"templates/verify_code.html"))
    # parse_encrypt_resume()
    # parse_encrypted_resume()
    
  
    # url = "http://yyht-api.996box.com/api/GameApi/getGiftList"
    # url = "http://127.0.0.1/cq/api"
    # secret_key = "7PZJImoeAE5Dnjb6pCYu8Ja5Buhb2urL"
    # data = {
    #     "domain": "",
    #     # "sign": secret_key,
    #     # "serverid": "1881",
    #     "rqtime": "1743884493",
    #     "rqrandom": "4iyw8p6hclIL00c68v057zD"
    # }
    # 计算签名
    # data_str =  CommonUtils.sort_para_to_str(data,ignore_empty_value=True)
    # data_str = f"{data_str}{secret_key}"#     data_str = "rqtime=1743884493&rqrandom=4iyw8p6hclIL00c68v057zD"
    # print(data_str)
    # sign = CommonUtils.calculate_md5(data_str,encoding='utf-8')
 
    # print(sign)



    # data['sign'] = sign

    # rsp = requests.post(url,json={})

    # print(rsp.text)
    # print(rsp.status_code)
    # print(rsp.json())
    # requests.post("http://127.0.0.1:6999",{"msgid":2008})
    # 初始化用户会话列表
    user_sessions = [
        {"uid": 123, "sid": "old-sid", "username": "报喜"}
    ]

    # 获取第一个用户并更新sid
    session = user_sessions[0]
    session['sid'] = "new-sid"

    # 验证结果
    print(user_sessions)
    # 输出: [{'uid': 123, 'sid': 'new-sid', 'username': '报喜'}]
    return
if __name__ == '__main__':
    main()

#  client  ---get_password_public_pem_req --->                 sdkserver
#  sdkserver  ---get_password_public_pem_rsp [public_pem]-->      client
#  client  ---login_req [username , encrypted password]--->    sdkserver
#  sdkserver  ---login_rsp [cookie(uid,token)]-->                 client 
#  client     ---get_userinfo_req[cookie(uid,token)] ----->           sdkserver


                    
#  sdkserver  ---get_userinfo_rsp [userinfo + combo_token]--------->                 client

# sdkserver  ------------ set combo_token_req   [combo_token account_uid game_uid]-----------------> gameserver


# client  ------------ check_combo_token-----------------> gameserver

# gateserver   <-转发协议-> gameserver
# dbserver  <-转发协议-> gameserver

# gameserver  <------------ other methods   [get_player_token_req rsp  ]-----------------> client

# gameserver  <------------ other methods   [player_login_req rsp  ]-----------------> client
# gameserver  <------------ other methods   [enter_scene_req rsp  ]-----------------> client
# gameserver  <------------ other methods   [load_scene_prefab_req rsp  ]-----------------> client
# .......  <------------ other methods   [other method player pos rot change notify  ]-----------------> client