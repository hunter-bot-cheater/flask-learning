from flask import Blueprint
#蓝图对象
od=Blueprint("order",__name__)


@od.route('/order/list')
def order_list():
    return "订单列表"

@od.route('/create/list')
def create_list():
    return "创建订单"


