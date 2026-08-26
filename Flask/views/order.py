from flask import Blueprint,session,render_template,request,redirect
from utils import db
from utils import cache
#蓝图对象
od=Blueprint("order",__name__)


@od.route('/order/list')
def order_list():

    user_info=session.get("user_info")
    role =user_info['role']
    real_name=user_info['real_name']
    if role==2:
        # select * from order
        data_list=db.fetch_all("select * from `order` left join userinfo on order.user_id=userinfo.id",[])
    else:
        # select * from order where user_id = user_info['id']
        data_list=db.fetch_all("select * from `order` left join userinfo on order.user_id=userinfo.id where order.user_id = %s",[user_info['id'],])


    status_dict={
        1:"待执行",
        2:"正在执行",
        3:"完成",
        4:"失败"
    }
    print(data_list)
    return render_template("order_list.html",data_list=data_list,status_dict=status_dict,real_name=real_name)


    return "订单列表"

@od.route('/order/create',methods=['GET','POST'])
def order_create():
    #创建订单逻辑
    if request.method=="GET":
        return render_template('order_create.html')

    url=request.form.get('url')
    count=request.form.get('count')

    #写入数据库
    user_info=session.get('user_info')
    params=[url,count,user_info['id']]
    order_id=db.insert("insert into `order` (url,count,user_id,status) values (%s,%s,%s,1)",params)
    print(order_id)

    #写入redis队列
    cache.push_queue(order_id)

    return redirect('/order/list')

@od.route('/order/delete')
def delete_list():
    return "删除订单"


