from flask import Flask,request,jsonify
import hashlib
app=Flask(__name__)

@app.route("/index",methods=["POST"]) #不加methods  不支持post 请求  默认只支持get请求
def index():

#约定发送的是post请求 且是json格式 {“ordered_string":"....."}
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
