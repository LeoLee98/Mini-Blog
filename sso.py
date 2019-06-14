from flask import Flask,session,request,make_response
from flask_session import Session
from redis import StrictRedis
import mysql.connector
import hashlib
app=Flask(__name__)

app.config['DEBUG']=True
app.config['SESSION_TYPE']='redis'
app.config['SESSION_REDIS']=StrictRedis(host='115.159.182.126', port=6379)    
Session(app)

db = mysql.connector.connect(user='root', password ='mysql199806', database='Blog',host = '115.159.182.126')


@app.route("/regist",methods = ["GET","POST"])
def regist():
    if request.method == 'POST':
        username = request.form['username']
        pwd = request.form['passwd']
        print(username,pwd)
    #生成hash并加盐
    md = hashlib.md5()
    md.update(username + "leo" + pwd)
    hashpwd = md.hexdigest()

    sql = "select * from User where username = '%s'" %(username)
    #查询是否已经注册
    cursor = db.cursor()
    cursor.execute(sql)
    detectBit = cursor.fetchone()
    if not detectBit:
        #如果没有就写进数据库
        sql = "INSERT INTO User(username, passwd) VALUES('%s','%s')" %(username, hashpwd)
        try:
            cursor.execute(sql)
            db.commit()
            resp = make_response("success")
            session['username'] = username
        except:
            db.rollback()
        
        return resp

    



if __name__=="__main__":
    app.run(port = 5555,debug=app.config['DEBUG'])