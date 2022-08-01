import os
from flask.config import Config

basedir = os.path.abspath(os.path.dirname(__file__)) #从os中获取当前文件夹的绝对路径 basdir存储数据库路径

class Config(object):
    SECRET_KEY=os.environ.get('SECERET_KEY') or 'A_GOOD_SECRET_KEY'#给wtf的密钥
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///'+ os.path.join(basedir,'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS=False

    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 25
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'ldq15598475682@163.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'XQEMWTWBTEBNEQQU'