from flask import Flask,request,jsonify
import hashlib
app=Flask(__name__)
# import uuid
# uuid.uuid4()
# UUID('e588aa79-0536-49e5-a202-60c2cbf6bdbb')
# 通过生成凭证，与用户传过来的凭证比对，才允许访问

def get_user_dict():
    with open("db.txt", mode='r', encoding='utf-8') as f:
        info_dict={}
        for line in f:
            line=line.strip()
            token,name=line.split(",")
            info_dict[token]=name
    return info_dict


@app.route("/index",methods=["POST"]) #不加methods  不支持post 请求  默认只支持get请求
def index():
    """
    请求的URL中需要携带  /index?token=88413692-41aa-4562-9c82-ce97dc26d93f
    约定发送的是post请求 且是json格式 {“ordered_string":"....."}


    """

    token=request.args.get("token")
    if not token:
        return jsonify({"status":"Flase",'error':"认证失败"})

    user_dict=get_user_dict()
    if token not in user_dict:
        return jsonify({"status": "Flase", 'error': "认证失败"})

    ordered_string=request.json.get("ordered_string")
    if not ordered_string:
        return jsonify({"status":False,'error':"参数错误"})
#调用核心算法，生成sign签名
    encrypt_string=ordered_string+"hjasdfjklajdadkjasd"
    obj=hashlib.md5(encrypt_string.encode('utf-8'))
    sign=obj.hexdigest()




    return jsonify({"status":True,'data':sign})



if __name__=='__main__':
    app.run(host="127.0.0.1",port=5000)
