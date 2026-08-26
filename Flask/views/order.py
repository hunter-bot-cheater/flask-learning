from flask import Blueprint,session,render_template
from utils import db
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

@od.route('/order/create')
def create_list():
    return "创建订单"

@od.route('/order/delete')
def delete_list():
    return "删除订单"


