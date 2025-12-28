import json


ErrorCode={
    0:"SUCCESS",
    -1:"SYSTEM ERROR",
    -2:"UNKNOWN ERROR",
    -3001:"DECRYPT ERROR",
    -3002:"PARAMETER ERROR",
    -3003:"DATABASE ERROR",
    -3004:"NETWORK ERROR",
    -3005:"AUTH ERROR",
    -3006:"AUTH TIMEOUT",
    -3007:"AUTH REFUSED",
    -3008:"AUTH EXPIRED",
    -3010:"USER NOT EXIST",
    -3011:"USER ALREADY EXIST",
    -3012:"USER PASSWORD ERROR",
    -3013:"SESSION ERROR",
    -3014:"SESSION TIMEOUT",
    -3015:"SESSION REFUSED",
    -3016:"SESSION EXPIRED",
    -3017:"SESSION NOT EXIST",
    -3018:"SESSION ALREADY EXIST",
    -3019:"TOKEN ERROR",
    -3021:"TOKEN REFUSED",
    -3022:"TOKEN EXPIRED",
    -3023:"CREATE VERIFY CODE ERROR",
    -3024:"VERIFY CODE ERROR",
    -3026:"VERIFY CODE EXPIRED",
}
ErrorCodeString={}
for k,v in ErrorCode.items():
    ErrorCodeString[v]=k



def get_response_json(code,msg=None,data = None):
    if msg:
        return {"retcode":code,"msg":msg,"data":data}
    else:
        return {"retcode":code,"msg":ErrorCode[code],"data":data}
def get_response_string(code,msg=None,data = None):
    if msg:
        return json.dumps({
            "retcode":code,
            "msg":msg,
            "data":data
            },ensure_ascii=False)
    else:
        return json.dumps(get_response_json(code = code,data=data),ensure_ascii=False)