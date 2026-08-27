from flask import Blueprint,render_template,request,redirect,session,flash

from utils import db
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
    user_dict=db.fetch_one("select * from userinfo where role=%s and mobile=%s and password=%s and is_deleted = 0",[role,mobile,pwd])
    print(user_dict)
    if user_dict:
        #登录成功+跳转
        session["user_info"]={"role":user_dict['role'],"real_name":user_dict['real_name'],"id":user_dict['id']}

        return redirect('/order/list')
    return render_template("login.html",error="用户名或密码错误")



@ac.route('/user/list')
def user_list():

    user_info=session.get('user_info')
    id=user_info['id']
    role=user_info['role']
    if role==2:#管理员 显示全部用户
        users=db.fetch_all("select * from userinfo where is_deleted = 0",[])
        print("管理员")
    elif role==1:
        user=db.fetch_one("select * from userinfo where id=%s and is_deleted = 0",[id,])
        users=[user] if user else []

    return render_template('user_list.html',users=users)



@ac.route('/user/update',methods=['GET','POST'])
def user_update():
    user_info = session.get('user_info')
    id = user_info['id']
    role = user_info['role']

    if request.method=='GET':
        edit_id = request.args.get('id')
        target_user = db.fetch_one("SELECT * FROM userinfo WHERE id=%s and is_deleted = 0", [edit_id])
        return render_template('user_update.html',role=role,user=target_user)


    edit_name=request.form.get("edit_name")
    edit_mobile=request.form.get("edit_mobile")
    edit_password=request.form.get("edit_password")
    edit_id=int(request.form.get("edit_id"))
    edit_role=request.form.get("edit_role")

    target_user = db.fetch_one("SELECT * FROM userinfo WHERE id=%s and is_deleted = 0", [edit_id])
    password=target_user['password']

    if edit_password and edit_password != password:
        db.update("update userinfo set password=%s where id=%s and is_deleted = 0",[edit_password,edit_id])
    if edit_password ==password:
        return render_template('user_update.html',role=role,user=target_user,error="新密码不能与原密码相同")

    if edit_mobile :
        db.update("update userinfo set mobile=%s where id=%s and is_deleted = 0",[edit_mobile,edit_id])
    if edit_name:
        db.update("update userinfo set real_name=%s where id =%s and is_deleted = 0",[edit_name,edit_id])

    if role==2:
        if edit_id==id and edit_role==1:
            return render_template('user_update.html',role=role,user=target_user,error="不能将自己设置为普通用户")
        if edit_role in ('1', '2'):
            db.update("update userinfo set role=%s where id=%s",[edit_role,edit_id])

    if id==edit_id:
        session['user_info']={"role":role,"real_name":edit_name,"id":edit_id}

    flash(f'用户 {target_user["real_name"]} 信息已编辑', 'success')
    return redirect('/user/list')


@ac.route('/user/delete/<int:delete_user_id>',methods=['POST'])
def user_delete(delete_user_id):
    user_info=session.get('user_info')
    role=user_info['role']
    user_id=user_info['id']
    if role!=2:
        flash('无权限执行此操作', 'danger')
        return redirect('/user/list')

    if user_id==delete_user_id:
        flash('不能删除自己', 'warning')
        return redirect('/user/list')

    target=db.fetch_one("select* from userinfo where id=%s and is_deleted=0",[delete_user_id,])
    if not target :
        flash('用户不存在', 'danger')
        return redirect('/user/list')

    delete_rows=db.update("update userinfo set is_deleted =1 where id=%s",[delete_user_id,])
    print(f"删除了{delete_rows}行")

    flash(f'用户 {target["real_name"]} 已删除', 'success')
    return redirect('/user/list')






