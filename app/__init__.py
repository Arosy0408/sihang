#导入所需的指令
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime   
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

from config import Config

app=Flask(__name__)
app.config.from_object(Config)

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
mail=Mail(app)
login=LoginManager(app)
login.login_view='login'#指定登录后的位置
login.login_message='登陆后浏览'
login.login_message_category='info'



from app.routes import*