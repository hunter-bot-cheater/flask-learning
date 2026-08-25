
import redis
REDIS_CONN_PARAMS={
    "host":'127.0.0.1',
    "password":'123456',
    "port":6379,
    "encoding":"utf-8",
    "protocol":2

}
conn=redis.Redis(**REDIS_CONN_PARAMS)
conn.lpush("test_spider_task_list",123)
# conn.lpush("test_spider_task_list",456)

# data=conn.rpop("test_spider_task_list")

data1=conn.brpop("test_spider_task_list",timeout=10) #在timeout等待时间内 如果队列有东西能拿 就立刻拿 最多等timeout秒
print(data1)#(b'test_spider_task_list', b'123')  元组

data1[1].decode('utf8')