# coding=utf-8
import sys
sys.path.append("..")
from sqlmodel.UserModel import User,db
from flask import Flask,request,jsonify,session,make_response
from flask_session import Session
from redis import StrictRedis
from datetime import timedelta
from flask_cors import CORS
import hashlib

app=Flask(__name__)
app.config['SESSION_TYPE']='redis'
app.config['SESSION_REDIS']=StrictRedis(host='115.159.182.126', port=6379) 
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes = 30)
Session(app)
CORS(app, supports_credentials=True)

@app.after_request
def af_request(resp):     
    """
    #请求钩子，在所有的请求发生后执行，加入headers。
    :param resp:
    :return:
    """
    resp = make_response(resp)
    resp.headers['Access-Control-Allow-Origin'] = 'http://115.236.123.247'
    resp.headers['Access-Control-Allow-Methods'] = 'GET,POST'
    resp.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return resp

@app.route("/sso/regist/",methods = ["POST"])
def regist():
    if request.method == 'POST':
        print(request.headers)
        print(request.form)
        userName = request.form['username']
        pwd = request.form['passwd']
        print(userName,pwd)
        #生成hash并加盐
        md = hashlib.md5()
        md.update((userName + "leo" + pwd).encode('utf-8'))
        hashPwd = md.hexdigest()
    
    #检测是否注册
        try:
            detectFlag = User.query.filter_by(username = userName).first()
        except:
            return jsonify({'code':500,'msg':'sqlserver error'})

        if  detectFlag == None:
            try:
                user = User(userName, hashPwd)
                db.session.add(user)
                db.session.commit()
                session['username'] = userName
                return jsonify({'code':0,'msg':'success regist'})
            except:
                db.rollback()
                print("rollback")
                return jsonify({'code':500,'msg':'sqlserver error'})
        else:
            return jsonify({'code':401,'msg':'account has been registed'})

@app.route("/sso/login/",methods = ["GET","POST"])
def login():
    if request.method == 'POST':
        print(request.headers)
        userName = request.form['username']
        pwd = request.form['passwd']
        #print(userName,pwd)
        #生成hash并加盐
        md = hashlib.md5()
        md.update((userName + "leo" + pwd).encode('utf-8'))
        hashPwd = md.hexdigest()

        #查询是否已经注册
        try:
            detectFlag = User.query.filter_by(username = userName).first()
        except:
            return jsonify({'code':500,'msg':'sqlserver error'})
        
        if not detectFlag:
            return jsonify({'code':402,'msg':'account has not been registed'})
        else:
            realPwd = detectFlag.passwd
            if hashPwd == realPwd:
                session['username'] = userName
                return jsonify({'code':0,'msg':'successfully login'})
            else:
                return jsonify({'code':404,'msg':'password wrong'})

@app.route("/sso/logout/",methods = ["GET","POST"])
def logout(): 
    #校验是否已经登录（为了防止接口攻击
    if 'username'not in session:
        return jsonify({'code':403,'msg':'please log in'})
    else:
        session.pop('username')
        return jsonify({'code':0,'msg':'successfully logout'})

@app.route("/sso/getInfo/",methods = ["GET"])
def getInfo(): 
    #校验是否已经登录（为了防止接口攻击
    if 'username'not in session:
        return jsonify({'code':403,'msg':'please log in'})
    else:
        return jsonify({'code':0,'msg':'successfully get','userName':'%s'%(session.get('username'))})


if __name__ == '__main__':
    app.run(port=4444, debug=True)