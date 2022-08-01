from unicodedata import category
from flask import Flask,render_template,flash,redirect,url_for,request
from app import app,bcrypt,db
from flask_login import login_url,login_required,current_user,login_user,logout_user
#导入 forms import User
from app.forms import RegisterForm,LoginForm,PasswordResetRequestform,ResetPasswordForm,PostTweetForm
from app.models import User,Post
from app.email import send_reset_password_mail



#创建路由
@app.route('/',methods=['GET','POST'])
@login_required
def index ():
    form = PostTweetForm()
    if form.validate_on_submit():
        body = form.text.data
        post = Post(body=body)
        current_user.posts.append(post)
        db.session.commit()
        flash('You have post a new tweet',category='success')
    n_followers = len(current_user.followers)
    n_followed = len(current_user.followed)
    page = request.args.get('page',1,type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(page,2,False)
    return render_template('index.html',form=form,posts=posts,n_followers=n_followers,n_followed=n_followed)
    #使用render_template调用其中的HTML文件

#创建登录页面路由
@app.route('/register', methods=['GET','POST'])
def register():
    title='注册'

    if current_user.is_authenticated:
        return redirect(url_for('index'))
        
    form=RegisterForm()
    if form.validate_on_submit():
        username=form.username.data
        email=form.email.data
        password=bcrypt.generate_password_hash(form.password.data)
        user = User(username=username,email=email,password=password)
        db.session.add(user)
        db.session.commit()
        flash('注册成功',category='success')
        return redirect(url_for('login'))

        #检测数据是否正常读取
        print(username,email,password)
    return render_template('register.html', title=title, form=form)#使用render_templ


@app.route('/login',methods=['GET','POST'])
def login():
    title='登录'
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form=LoginForm()
    if form.validate_on_submit():
        username=form.username.data
        password=form.password.data
        remember=form.remember.data
        #检查密码是否输入正确
        user=User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password,password):
            login_user(user,remember=remember)
            flash('登陆成功',category='info')
            if request.args.get('next'):
                next_page=request.args.get('next')
                return redirect(next_page)
            return redirect(url_for('index'))
        flash('用户名不存在或密码不正确',category='danger')
    
    return render_template('login.html',title=title,form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/send_password_reset_request',methods=['GET','POST'])
def send_password_reset_request():
    if current_user.is_authenticated:#判断用户是否已经登陆
        return redirect(url_for('index'))
    form = PasswordResetRequestform()
    if form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email=email).first()
        token = user.generate_reset_password_token()
        send_reset_password_mail(user,token)
        flash('邮箱已发送，请查收',category='info')
    return render_template('send_password_reset_request.html',form=form)

@app.route('/reset_password',methods=['GET','POST'])
def reset_password():
    if current_user.is_authenticated:#判断用户是否登录
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    return render_template('reset_password.html',form=form)

@app.route('/reset_password<token>',methods=['GET','POST'])
def reset_possword(token):
    if current_user.is_authenticated:#判断新用户是否已经登陆
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user=User.check_reset_password_token(token)
        if user:
            user.password=bcrypt.generate_password_hash(form.password.data)
            db.session.commit()
            flash('Your password reset is done,you can login now',category='info')
            return redirect(url_for('login'))
        else:
            flash('Then user is not exist',category='info')
            return redirect(url_for('login'))
    return render_template('reset_password.html',form=form)

