# coding=utf-8
import os 
import sys
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) #该执行模块所在文件夹的父文件夹
Root_DIR = os.path.dirname(BASE_DIR) #该执行模块文件夹的父文件夹即项目根目录
sys.path.append(Root_DIR)
from sqlmodel.UserModel import User,db
from flask import Flask,request,jsonify,session,make_response
from flask_session import Session
from redis import StrictRedis
from datetime import timedelta
from flask_cors import CORS
import hashlib
import logging
import json


#读取配置
with open(os.path.join(Root_DIR, "config.json"),'r') as load_f:
    load_dict = json.load(load_f)

app=Flask(__name__)
app.config['SESSION_TYPE']='redis'
app.config['SESSION_REDIS']=StrictRedis(host=load_dict['redis_ip'], port=6379) 
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes = 30)
Session(app)
CORS(app, supports_credentials=True)

logging.basicConfig(level=logging.DEBUG,
                    filename=os.path.join(Root_DIR, 'log/sso.log'),
                    datefmt='%Y/%m/%d %H:%M:%S',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(module)s - %(message)s')
logger = logging.getLogger('sso')

@app.after_request
def af_request(resp):     
    """
    #请求钩子，在所有的请求发生后执行，加入headers。
    :param resp:
    :return:
    """
    resp = make_response(resp)
    resp.headers['Access-Control-Allow-Origin'] = load_dict['Access-Control-Allow-Origin']
    resp.headers['Access-Control-Allow-Origin'] = request.headers.get('Origin')
    resp.headers['Access-Control-Allow-Headers'] = load_dict['Access-Control-Allow-Headers']
    resp.headers['Access-Control-Allow-Methods'] = 'GET,POST'
    resp.headers['Access-Control-Allow-Credentials'] = 'true'
    resp.headers['Cache-Control'] = 'no-cache'
    return resp

@app.route("/sso/regist/",methods = ["POST"])
def regist():
    if request.method == 'POST':
        userName = request.form['username']
        pwd = request.form['passwd']
        #生成hash并加盐
        md = hashlib.md5()
        md.update((userName + "leo" + pwd).encode('utf-8'))
        hashPwd = md.hexdigest()
    
    #检测是否注册
        try:
            db.session.commit()
            detectFlag = User.query.filter_by(username = userName).first()
        except Exception as e :
            logger.info(e,exc_info=True)
            return jsonify({'code':500,'msg':'sqlserver error'})

        if  detectFlag == None:
            try:
                user = User(userName, hashPwd)
                db.session.add(user)
                db.session.commit()
                session['username'] = userName
                return jsonify({'code':0,'msg':'success regist'})
            except Exception as e:
                logger.info(e,exc_info=True)
                db.session.rollback()
                return jsonify({'code':500,'msg':'sqlserver error'})
        else:
            return jsonify({'code':401,'msg':'account has been registed'})

@app.route("/sso/login/",methods = ["GET","POST"])
def login():
    if request.method == 'POST':
        userName = request.form['username']
        pwd = request.form['passwd']
        #print(userName,pwd)
        #生成hash并加盐
        md = hashlib.md5()
        md.update((userName + "leo" + pwd).encode('utf-8'))
        hashPwd = md.hexdigest()

        #查询是否已经注册
        try:
            db.session.commit()
            detectFlag = User.query.filter_by(username = userName).first()
        except Exception as e:
            logger.info(e,exc_info=True)
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
    app.run(host = '0.0.0.0', port=4444, debug=True)