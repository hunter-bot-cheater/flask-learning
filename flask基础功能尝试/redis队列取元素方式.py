import redis

from utils import cache


POOL=redis.ConnectionPool(host='127.0.0.1', port=6379, password='123456',encoding="utf-8",protocol=2,  decode_responses=True,max_connections=100)



def fetch_total_queue():
    # 方式一：全部获取redis队列里当前的所有
    # conn=redis.Redis(connection_pool=POOL)
    # total_count=conn.llen("DAY21_TASK_QUEUE")
    # conn.lrange("DAY21_TASK_QUEUE",start=0,end=total_count)
    #方式二：逐一获取
    # conn=redis.Redis(connection_pool=POOL)
    # total_count=conn.llen("DAY21_TASK_QUEUE")
    # for index in range(total_count):
    #     e=conn.lindex("DAY21_TASK_QUEUE",index)
    #     print(e)
    #方式三：一次取一部分
    conn=redis.Redis(connection_pool=POOL)
    total_count=conn.llen("DAY21_TASK_QUEUE")

    has_fetch_count=0
    while has_fetch_count<total_count:
        ele_list=conn.lrange("DAY21_TASK_QUEUE",has_fetch_count,has_fetch_count+3)
        has_fetch_count=has_fetch_count+len(ele_list)


if __name__ == '__main__':
    for i in range(5):
        cache.push_queue(i)
    fetch_total_queue()
