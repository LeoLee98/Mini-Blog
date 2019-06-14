from flask import Flask,session,request,make_response,jsonify
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


@app.route("/sso/regist",methods = ["GET","POST"])
def regist():
    if request.method == 'POST':
        userName = request.form['username']
        pwd = request.form['passwd']
        #print(userName,pwd)
        #生成hash并加盐
        md = hashlib.md5()
        md.update((userName + "leo" + pwd).encode('utf-8'))
        hashPwd = md.hexdigest()

        sql = "select * from User where username = '%s'" %(userName)
        #查询是否已经注册
        try:
            cursor = db.cursor()
            cursor.execute(sql)
            detectBit = cursor.fetchone()
        except:
            return jsonify({'code':500,'msg':'sqlserver error'})
        if not detectBit:
            #如果没有就写进数据库
            sql = "INSERT INTO User(username, passwd) VALUES('%s','%s')" %(userName, hashPwd)
            try:
                cursor.execute(sql)
                db.commit()
                session['username'] = userName
                print("commit")
                return jsonify({'code':0,'msg':'success regist'})
            except:
                db.rollback()
                print("rollback")
                return jsonify({'code':500,'msg':'sqlserver error'})
        else:
            return jsonify({'code':401,'msg':'account has been registed'})

@app.route("/sso/login",methods = ["GET","POST"])
def login():
    if request.method == 'POST':
        userName = request.form['username']
        pwd = request.form['passwd']
        #print(userName,pwd)
        #生成hash并加盐
        md = hashlib.md5()
        md.update((userName + "leo" + pwd).encode('utf-8'))
        hashPwd = md.hexdigest()

        sql = "select * from User where username = '%s'" %(userName)
        #查询是否已经注册
        try:
            cursor = db.cursor()
            cursor.execute(sql)
            detectBit = cursor.fetchone()
        except:
            return jsonify({'code':500,'msg':'sqlserver error'})
        
        if not detectBit:
            return jsonify({'code':402,'msg':'account has not been registed'})
        else:
            sql = "select passwd from User where username = '%s'" %userName
            try:
                cursor.execute(sql)
                realPwd = cursor.fetchone()[0]
                #print (realPwd)
                if hashPwd == realPwd:
                    session['username'] = userName
                    return jsonify({'code':0,'msg':'successfully login'})
                else:
                    return jsonify({'code':404,'msg':'password wrong'})
            except:
                return jsonify({'code':500,'msg':'sqlserver error'})
                
@app.route("/api/v1/logout",methods = ["GET","POST"])
def logout(): 
    #校验是否已经登录（为了防止接口攻击
    if 'username'not in session:
        return jsonify({'code':403,'msg':'please log in'})
    else:
        session.pop('username')
        return jsonify({'code':0,'msg':'successfully logout'})
        

    



if __name__=="__main__":
    app.run(port = 5555,debug=app.config['DEBUG'])