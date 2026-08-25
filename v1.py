from flask import Flask,request

app=Flask(__name__)


#http://127.0.0.1:5000/index    执行index GET请求
#http://127.0.0.1:5000/index?age=19&pwd=123   GET请求

#请求体：xx=123&yy=999
#请求体:{"xx":123,"yy":999}  JSON格式


@app.route("/index",methods=["POST","GET"]) #不加methods  不支持post 请求  默认只支持get请求
def index():
    age=request.args.get("age")  #在URL中获取相关参数数据
    pwd=request.args.get("pwd")
    print(age,pwd)

    xx=request.form.get("xx")  #在请求体中获取相关参数 ，接受不了JSON格式的数据
    yy=request.form.get("yy")

#data = {"name": "张三", "info": {"city": "南京"}}
    data=request.json
    name=data["name"]

    age=data.get("age")
    city=data.get("info",{}).get("city")  #字典中有字典 第一个get里的{} 防止JSON里没有INFO字段而报错


    #调用核心算法，生成sign签名

    import json
    return json.dumps({"status":True,'data':"asedcasd"})  #json.dumps将字典转化为json格式的字符串  '{"status": true, "data": "asedcasd"}'
    return json.dumps({"status":False,'error':"vasdavasd"})

    #也可以用jsonify return jsonify({"status":True,'data':"fasdaqsad"}) 自动设置正确的 application/json 响应头

@app.route("/home")
def home():
    return "失败"

if __name__=='__main__':
    app.run(host="127.0.0.1",port=5000)
