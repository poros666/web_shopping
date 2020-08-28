from flask import Flask, render_template, request, jsonify, redirect
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_mongoengine import MongoEngine
from models import *
import json
import time

# 创建flask对象
app = Flask(__name__, template_folder="templates", static_folder="static")
app.config.from_object("config")

# 使用flask_login
loginmanager = LoginManager(app)
loginmanager.session_protection = "strong"
loginmanager.login_view = "login"

# 利用MongoEngine来使用MongoDB
db = MongoEngine(app)


@loginmanager.user_loader
def get_user(user_id):
    return User.objects(id=user_id).first()


# 配置路由


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")


@app.route("/")
@login_required
def index():
    return render_template("homepage.html")


@app.route("/add", methods=["POST", "GET"])
@login_required
def add_proc():
    if request.method == "GET":
        return render_template("homepage.html")
    elif request.method == "POST":
        param = json.loads(request.data.decode("utf-8"))
        pid = param.get("pid", "")
        print("add_prodc", pid)
        user = current_user
        print("before add:", "pid", pid, "nickname:", user.nickname, "cart:", user.cart)
        count = user.cart[0]["p%d" % pid]
        user.cart[0]["p%d" % pid] = count + 1
        user.save()
        print("after add:", "pid", pid, "nickname:", user.nickname, "cart:", user.cart)
    return jsonify({
        "result": "OK"
    })


@app.route("/delete", methods=["POST", "GET"])
@login_required
def delete_proc():
    if request.method == "GET":
        return render_template("shoppingcar.html")
    elif request.method == "POST":
        param = json.loads(request.data.decode("utf-8"))
        pid = param.get("pid", "")
        print(pid)
        user = current_user
        print("pid", pid, "nickname:", user.nickname, "cart:", user.cart)
        user.cart[0]["p%d" % pid] = 0
        user.save()
    # print(user.cart["0"])
    return jsonify({
        "result": "OK"
    })


@app.route("/create", methods=["POST", "GET"])
@login_required
def create_order():
    if request.method == "GET":
        return render_template("orderhis.html")
    elif request.method == "POST":
        param = json.loads(request.data.decode("utf-8"))
        pid = param.get("pid", "")
        print(pid)
        user = current_user
        print("before create:", "pid", pid, "nickname:", user.nickname, "cart:", user.cart, "his:", user.his)

        total = 10 * user.cart[0]["p1"] + \
                20 * user.cart[0]["p2"] + \
                30 * user.cart[0]["p3"] + \
                40 * user.cart[0]["p4"] + \
                50 * user.cart[0]["p5"]
        order_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        user.his.append({"order_time": order_time, "total": total})
        user.cart[0]["p1"] = 0
        user.cart[0]["p2"] = 0
        user.cart[0]["p3"] = 0
        user.cart[0]["p4"] = 0
        user.cart[0]["p5"] = 0
        user.save()
        print("after create:", "pid", pid, "nickname:", user.nickname, "cart:", user.cart, "his:", user.his)

    return jsonify({
        "result": "OK"
    })


@app.route("/shoppingcar")
@login_required
def shopping():
    return render_template("shoppingcar.html")


@app.route("/orderhis")
@login_required
def order():
    return render_template("orderhis.html")


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":
        err_msg = {
            "result": "NO"
        }
        param = json.loads(request.data.decode("utf-8"))
        username = param.get("username", "")
        password = param.get("password", "")
        nickname = param.get("nickname", "")
        if not username:
            err_msg["msg"] = "缺少用户名"
            return jsonify(err_msg)
        if not password:
            err_msg["msg"] = "缺少密码"
            return jsonify(err_msg)
        if not nickname:
            err_msg["msg"] = "缺少用户名"
            return jsonify(err_msg)
        user = User.objects(username=username)
        if not user:
            user = User(username=username, nickname=nickname)
            user.hash_password(password)
            print("register", user.nickname, user.cart)
            user.cart[0]["p1"] = 0
            user.cart[0]["p2"] = 0
            user.cart[0]["p3"] = 0
            user.cart[0]["p4"] = 0
            user.cart[0]["p5"] = 0
            user.save()
            print("after register", user.nickname, user.cart)
            return jsonify({
                "result": "OK",
            })
        else:
            err_msg["msg"] = "用户已经注册"
            return jsonify(err_msg)


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        err_msg = {
            "result": "NO"
        }
        param = json.loads(request.data.decode("utf-8"))
        username = param.get("username", "")
        password = param.get("password", "")
        if not username:
            err_msg["msg"] = "缺少用户名"
            return jsonify(err_msg)
        if not password:
            err_msg["msg"] = "缺少密码"
            return jsonify(err_msg)
        user = User.objects(username=username).first()
        if not user:
            err_msg["msg"] = "用户尚未注册"
            return jsonify(err_msg)
        if not user.verify_password(password):
            err_msg["msg"] = "密码错误"
            return jsonify(err_msg)
        print(user.cart[0])
        login_user(user)
        return jsonify({
            "result": "OK",
            "next_url": "/"
        })


if __name__ == '__main__':
    app.run()
