from app import app

#开启debug模式
#使用port指定地址
#指定host为0.0.0.0允许外部访问
if __name__=='__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
    