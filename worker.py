"""

worker作用：
去队列中获取任务，执行并写入结果队列
"""
import redis
import json
import hashlib
import time
def get_task():
    REDIS_CONN_PARAMS = {
        "host": '127.0.0.1',
        "password": '123456',
        "port": 6379,
        "encoding": "utf-8",
        "protocol": 2,
        "socket_timeout": None,

    }
    conn = redis.Redis(**REDIS_CONN_PARAMS)

    data = conn.brpop("spider_task_list", timeout=10)  # 在timeout等待时间内 如果队列有东西能拿 就立刻拿 最多等timeout秒
    if not data:
        return
    return json.loads(data[1].decode('utf8'))  #json.loads将json字符串 ‘{"tid":tid,'data':ordered_string}'转换为字典{"tid":tid,'data':ordered_string}

def set_result(tid,value):
    REDIS_CONN_PARAMS = {
        "host": '127.0.0.1',
        "password": '123456',
        "port": 6379,
        "encoding": "utf-8",
        "protocol": 2,
        "socket_timeout": None,

    }
    conn=redis.Redis(**REDIS_CONN_PARAMS)
    conn.hset("spider_result_list",tid,value)

def run():
    while True:
        #1.获取任务
        task_dict=get_task()
        print(task_dict)
        if not task_dict:
            time.sleep(1)
            continue
        #2.执行耗时操作
        #{"tid":'xxx','data':"...."}
        ordered_string=task_dict['data']
        encrypt_string = ordered_string + "hjasdfjklajdadkjasd"
        obj = hashlib.md5(encrypt_string.encode('utf-8'))
        sign = obj.hexdigest()


        #写入结果队列 (redis的hash)
        tid= task_dict['tid']
        set_result(tid,sign)

if __name__ == "__main__":
    run()

