from flask import Blueprint,session,redirect
#蓝图对象
od=Blueprint("order",__name__)


@od.route('/order/list')
def order_list():

    #读取cookie 解密 获取用户信息
    user_info=session.get("user_info")
    if not user_info:
        return redirect('/login')

    return "订单列表"

@od.route('/order/create')
def create_list():
    return "创建订单"

@od.route('/order/delete')
def delete_list():
    return "删除订单"


