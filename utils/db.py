from dbutils.pooled_db import PooledDB
import pymysql
from pymysql import cursors

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


def fetch_one(sql,params):
    conn=POOL.connection()
    cursor=conn.cursor(cursor=cursors.DictCursor) #加了这个 返回的result才是字典
    cursor.execute(sql,params)
    result=cursor.fetchone()
    cursor.close()
    conn.close()

    return result

def fetch_all(sql,params):
    conn=POOL.connection()
    cursor=conn.cursor(cursor=cursors.DictCursor) #加了这个 返回的result才是字典
    cursor.execute(sql,params)
    result=cursor.fetchall()
    cursor.close()
    conn.close()

    return result



def insert(sql,params):
    conn=POOL.connection()
    cursor=conn.cursor(cursor=cursors.DictCursor) #加了这个 返回的result才是字典
    cursor.execute(sql,params)
    conn.commit()
    cursor.close()
    conn.close()
    return cursor.lastrowid  #新生成的数据的id


def update(sql,params):
    conn=POOL.connection()
    cursor=conn.cursor()
    cursor.execute(sql,params)
    conn.commit()
    affected_rows=cursor.rowcount
    cursor.close()
    conn.close()

    return affected_rows
