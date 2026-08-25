from flask import Flask,request,jsonify
import hashlib
import pymysql
from dbutils.pooled_db import PooledDB
import uuid
import redis
import json

REDIS_CONN_PARAMS = {
        "host": '127.0.0.1',
        "password": '123456',
        "port": 6379,
        "encoding": "utf-8",
        "protocol": 2,
        "socket_timeout": None,

    }


REDIS_POOL=redis.ConnectionPool(host='127.0.0.1',
                                password='123456',
                                port=6379, encoding='utf-8',
                                protocol=2,
                                socket_timeout=None,
                                decode_responses=True,
                                max_connections=100)


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

app=Flask(__name__)
# import uuid
# uuid.uuid4()
# UUID('e588aa79-0536-49e5-a202-60c2cbf6bdbb')
# 通过生成凭证，与用户传过来的凭证比对，才允许访问


def fetch_one(sql,params):

    # conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='flask-learning',
    #                        charset='utf8mb4')
    conn = POOL.connection()  #从连接池里抓取一个链接
    cursor = conn.cursor()
    try:
        cursor.execute(sql,params)  # [token],[token,](token,) 都行 把token传入%s 防止sql注入 (token) 这样不行 不是元组
        result = cursor.fetchone()

        return result
    finally:
        cursor.close()
        conn.close()  #不是关闭链接 将此链接交还给连接池  ,即使报错 也会把链接还给连接池


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


@app.route("/task",methods=["POST"])
def task():

    oredered_string=request.json.get("ordered_string")
    if not oredered_string:
        return jsonify({"status":False,'error':"参数错误"})

    #生成任务id
    tid=str(uuid.uuid4())
    #1.放入到队列
    task_dict={'tid':tid,'data':oredered_string}

    conn=redis.Redis(connection_pool=REDIS_POOL)
    conn.lpush("spider_task_list",json.dumps(task_dict))  #把字典转化为json字符串 加入到队列

    #2.给用户返回任务

    return jsonify({"status":True,"tid":tid,'message':"正在处理中，预计1分钟"})


@app.route("/result",methods=["GET"])
def result():
    #/result?tid=.....
    tid=request.args.get("tid")
    if not tid:
        return jsonify({"status":False,'error':"参数错误"})

    conn = redis.Redis(**REDIS_CONN_PARAMS)
    sign=conn.hget("spider_result_list",tid)
    if not sign:
        return jsonify({"status":True,'data':"","message":"未完成，请继续等待"})
    sign_string=sign.decode('utf-8')
    conn.hdel("spider_result_list",tid)  #拿取一次后就在结果队列中删除该tid和对应的data
    print(sign_string)

    return jsonify({"status":True,'data':sign_string})
if __name__=='__main__':
    app.run(host="127.0.0.1",port=5000)
