import redis

POOL=redis.ConnectionPool(host='127.0.0.1', port=6379, password='123456',encoding="utf-8",protocol=2,  decode_responses=True,max_connections=100)

def push_queue(value):
    conn=redis.Redis(connection_pool=POOL)
    conn.lpush("DAY21_TASK_QUEUE",value)