from flask import Flask,request,jsonify
import hashlib
import pymysql
app=Flask(__name__)
# import uuid
# uuid.uuid4()
# UUID('e588aa79-0536-49e5-a202-60c2cbf6bdbb')
# 通过生成凭证，与用户传过来的凭证比对，才允许访问


def fetch_one(sql,params):

    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='flask-learning',
                           charset='utf8mb4')
    cursor = conn.cursor()
    cursor.execute(sql,params)  # [token],[token,](token,) 都行 把token传入%s 防止sql注入 (token) 这样不行 不是元组
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result


@app.route("/index",methods=["POST"]) #不加methods  不支持post 请求  默认只支持get请求
def index():
    """
    请求的URL中需要携带  /index?token=88413692-41aa-4562-9c82-ce97dc26d93f
    约定发送的是post请求 且是json格式 {“ordered_string":"....."}


    """
    token=request.args.get("token")
    #1.token是否为空
    if not token:
        return jsonify({"status":"Flase",'error':"认证失败"})
    #2.token是否合法，链接mysql进行操作
    result=fetch_one("select * from user where token=%s",[token,])


    if not result:
        return jsonify({"status": "False", 'error': "认证失败"})

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
