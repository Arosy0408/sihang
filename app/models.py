from email.policy import default
from hashlib import algorithms_available
from sqlite3 import Timestamp
from flask_login import UserMixin
from app import db,datetime,login
from flask import current_app
import jwt

#获取用户输入
@login.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()    

followers = db.Table('followers',
    db.Column('follower_id',db.Integer,db.ForeignKey('user.id')),
    db.Column('followed_id',db.Integer,db.ForeignKey('user.id')),)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(80),unique=True,nullable=False)#unique（不可以相同) nullabie(是否为空)
    email = db.Column(db.String(120),unique=True,nullable=False)
    avatar_img = db.Column(db.String(120),default='/static/assest/default_avatar.jpg',nullable=False)
    password = db.Column(db.String(120),nullable=False)
    
    posts = db.relationship('Post',backref=db.backref('author',lazy=True))
    #关注与被关注用户的关系处理
    followed= db.relationship(
        'User',secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.follower_id == id),
        backref = db.backref('followers',lazy=True),lazy=True
    )

    def __reper__(self):
        return'<User %r>' % self.username

    def generate_reset_password_token(self):
        return jwt.encode({'id':self.id},current_app.config['SECRET_KEY'],algorithm='HS256')

    # def check_reset_password_token(self,token):
    #     try:
    #         data = jwt.decode(token,current_app.config['SECRET_KEY'],algorithms=['HS256'])
    #         return User.query.filter_by(id=data['id']).first()
    #     except:
    #         return

    #加密尝试设置密码的用户信息
    @staticmethod
    def check_reset_passsword_token(token):
        try:
            data = jwt.decode(token,current_app.config['SECRET_KEY'],algorithms=['HS256'])
            return User.query.filer_by(id=data['id']).first()
        except:
            return


    def follow(self,user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self,user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self,user):
        return self.followed.filter(followers.c.follower_id == user.id).count()>0        

class Post(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    body = db.Column(db.String(140),nullable=False)
    timestamp = db.Column(db.DateTime,default=datetime.now)

    user_id =db.Column( db.Integer,db.ForeignKey('user.id'),nullable=False)

    def _repr_(self):
        return '<Post {}>'.format(self.body)








