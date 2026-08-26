from flask import Flask,request,session,redirect
import os
def auth():#拦截器 没有session.get("user_info")值的人前置拦截
     if request.path.startswith("/static"):
         return

     if request.path =="/login":
         #继续执行 不拦截
        return

     user_info=session.get("user_info")
     if user_info:
         #说明已经登录 继续执行
         return

     return redirect("/login") #未登录 跳转回登录页面


def create_app():
    app=Flask(__name__)
    app.secret_key=os.getenv("SECRET_KEY")
    from .views import account
    from .views import order
    app.register_blueprint(account.ac)
    app.register_blueprint(order.od)

    app.before_request(auth)
    return app