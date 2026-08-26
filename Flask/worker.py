import redis
import time
from utils import db,cache
from concurrent.futures import ThreadPoolExecutor



def db_queue_init():
    db_id_list=[]
    db_list=db.fetch_all("select * from `order` where status=1",[])
    for item in db_list:
        db_id_list.append(item["id"])

    #去redis里取
    cache_str_list=cache.fetch_total_queue()
    cache_int_list=[int(item) for item in cache_str_list]

    #找数据库列表里有的  redis列表里没有的  然后放入redis
    need_push=sorted(set(db_id_list)-set(cache_int_list)) #升序排列 推入队列的时候小id优先被推入 靠右 优先被brpop执行
    if need_push:
        cache.push_queue(*need_push)

def get_order_object(order_id):
    res=db.fetch_one("select * from `order` where id=%s",[order_id,])

    return res

def update_order_status(order_id,status):#更新订单状态
    db.update("update `order` set status=%s where id=%s",[status,order_id])

def task():
    pass

def run():
    #没有与redis队列中的相比较
    # undo_orders=db.fetch_all("select * from `order` where status=1",[])
    # for item in undo_orders:
    #     order_id=item["id"]
    #     cache.push_queue(order_id)


    #初始化数据库未在队列的订单
    db_queue_init()

    while True:

        order_id=cache.pop_queue()

        print(order_id)
        if not order_id:
            time.sleep(1)
            continue

        #订单是否存在
        order_dict=get_order_object(order_id)
        if not order_dict:
            print("订单不存在")
            continue

        #根据订单id去执行任务
        #订单状态显示为正在执行 status=2
        update_order_status(order_id,2)

        #执行任务代码
        print("执行任务订单：",order_dict)
        thread_pool=ThreadPoolExecutor(max_workers=30)
        for i in range (order_dict['count']):
            thread_pool.submit(task,order_dict)
        thread_pool.shutdown()



        #执行完成，将数据库相应的订单的status=3
        update_order_status(order_id,3)


if __name__ == '__main__':
    run()