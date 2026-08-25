import requests

res=requests.post(url="http://127.0.0.1:5000/index",
              json={"ordered_string":"1234534123"})

#我手动用户的json数据 向外部服务器发送请求 然后返回res结果

print(res.json())


#request 用来接收用户发来的请求  要from flask import request

#requests 主动调用第三方服务   直接import requests
