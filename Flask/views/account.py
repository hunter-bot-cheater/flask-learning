from flask import Blueprint,render_template,request,redirect
import pymysql
#蓝图对象
ac=Blueprint("account",__name__)


@ac.route('/login',methods=['GET','POST'])  #methods只能是大写
def login():
    if request.method=="GET":
        return render_template("login.html")
    role=request.form.get("role")
    mobile=request.form.get("mobile")
    pwd=request.form.get("pwd")

    print(role, mobile, pwd)

    # 链接mysql 并执行sql语句查询用户名密码是否正确
    conn=pymysql.connect(host='127.0.0.1',port=3306,user='root',password='123456',charset='utf8mb4',db='flask-learning')
    cursor=conn.cursor()
    cursor.execute("select * from userinfo where role=%s and mobile=%s and password=%s",[role,mobile,pwd])
    user_dict=cursor.fetchone()
    cursor.close()
    conn.close()

    if user_dict:
        return redirect('/order/list')
    return render_template("login.html",error="用户名或密码错误")







    return "ok"
@ac.route('/users')
def users():
    return "用户列表"