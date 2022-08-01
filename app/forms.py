from decimal import Subnormal
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired,Length,EqualTo,ValidationError,Email
from app.models import User

class RegisterForm(FlaskForm):
    username=StringField('username',validators=[DataRequired(),Length(min=6,max=18)])
    email=StringField('邮箱地址',validators=[DataRequired()])
    password=PasswordField('密码',validators=[DataRequired(),Length(min=8,max=20)])
    confirm=PasswordField('重复密码',validators=[DataRequired(),EqualTo('password')])
    submit=SubmitField('注册')#摁扭

    def validate_nsername(self,username):
        user=User.query.filter_by(username=username.data).first()   
        if user:
            raise ValidationError('用户名已被占用')


    def validate_email(self,email):
        email=User.query.filter_by(email=email.data).first()   
        if email:
            raise ValidationError('邮箱地址已被占用')

class LoginForm(FlaskForm):

    username=StringField('Username',validators=[DataRequired(),Length(min=6,max=18)])
    password=PasswordField('Password',validators=[DataRequired(),Length(min=8,max=20)])
    remember=BooleanField('remember')
    submit=SubmitField('登录')#摁扭

class PasswordResetRequestform(FlaskForm):

    email=StringField('Email',validators=[DataRequired(),Email()])
    submit=SubmitField('确认')                          

    def find_email(self,email):
        email=User.query.filter_by(email=email.data).first()   
        if not email:
            raise ValidationError('邮箱不存在，你丫再想想')

class ResetPasswordForm(FlaskForm):

    password = PasswordField('password',validators=[DataRequired(),Length(min=8,max=20)])
    confirm = PasswordField('Repet Password',validators=[DataRequired(),EqualTo('password')])
    submit=SubmitField('重设密码')

class PostTweetForm(FlaskForm):

    text = TextAreaField('Say something...',validators = [DataRequired(),Length(min=1,max=140)])
    submit = SubmitField('Post Test')