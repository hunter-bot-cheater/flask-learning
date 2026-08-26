from flask import Blueprint,session,redirect
#蓝图对象
od=Blueprint("order",__name__)


@od.route('/order/list')
def order_list():

    return "订单列表"

@od.route('/order/create')
def create_list():
    return "创建订单"

@od.route('/order/delete')
def delete_list():
    return "删除订单"


