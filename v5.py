from flask import Flask,request,jsonify
import hashlib
import pymysql
from dbutils.pooled_db import PooledDB


app=Flask(__name__)

POOL = PooledDB(
    creator=pymysql,               # 指定使用 PyMySQL 驱动
    maxconnections=10,             # 连接池允许的最大连接数（硬上限）
    mincached=2,                   # 启动时预先创建的“空闲连接”数
    maxcached=3,                   # 池中允许保留的最大“空闲连接”数
    blocking=True,                 # 连接不够时是否阻塞等待 等待有链接返回到连接池
    setsession=[],                 # 连接建立后执行的初始化 SQL（如设置时区）
    ping=0,                        # 连接健康检查策略（0 代表不检查）
    # **settings.MYSQL_CONN_PARAMS   解包主机、端口、账号密码等
    host='127.0.0.1',
    port=3306, user='root',
    passwd='123456',
    db='flask-learning',
    charset='utf8mb4'
)


# import uuid
# uuid.uuid4()
# UUID('e588aa79-0536-49e5-a202-60c2cbf6bdbb')
# 通过生成凭证，与用户传过来的凭证比对，才允许访问


def fetch_one(sql,params):

    # conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='flask-learning',
    #                        charset='utf8mb4')
    conn = POOL.connection()  #从连接池里抓取一个链接
    cursor = conn.cursor()
    cursor.execute(sql,params)  # [token],[token,](token,) 都行 把token传入%s 防止sql注入 (token) 这样不行 不是元组
    result = cursor.fetchone()
    cursor.close()
    conn.close()  #不是关闭链接 将此链接交还给连接池 
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
