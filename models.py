from app import app, db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Document, UserMixin):
    # 元数据
    meta = {
        "collection": "user",
        "ordering": ["-id"],
        "strict": True
    }
    username = db.StringField()  # 用户名
    password_hash = db.StringField()  # 密码
    nickname = db.StringField()  # 昵称
    floder = db.StringField()  # 暂时没用到的废案
    superuser = db.BooleanField(default=False)  # 暂时没用到的废案
    p1 = db.IntField(default=0)  # 第一种物品
    p2 = db.IntField(default=0)  # 第二种物品
    p3 = db.IntField(default=0)  # 第三种物品
    p4 = db.IntField(default=0)  # 第四种物品
    p5 = db.IntField(default=0)  # 第五种物品
    count = db.IntField(default=0)  # 历史记录数(废案)
    cart = db.ListField(default=[{}])  # 购物车
    his = db.ListField(default=[{}])  # 历史记录

    def hash_password(self, password):
        self.password_hash = generate_password_hash(password)
        self.save()

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

