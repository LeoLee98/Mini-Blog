# coding=utf-8
import os 
import sys
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) #该执行模块所在文件夹的父文件夹
Root_DIR = os.path.dirname(BASE_DIR) #该执行模块文件夹的父文件夹即项目根目录
sys.path.append(Root_DIR)
from sqlmodel.UserModel import User,Blog,BlogComment,db,checkStr,checkInt
from flask import Flask,request,jsonify,session,make_response,abort
from flask_session import Session
from redis import StrictRedis
from datetime import timedelta
from flask_cors import CORS
import datetime
import hashlib
import logging
import requests
import logging
import json


from flask import _request_ctx_stack as stack

#读取配置
with open(os.path.join(Root_DIR, "config.json"),'r') as load_f:
    load_dict = json.load(load_f)

app=Flask(__name__)
app.config['SESSION_TYPE']='redis'
app.config['SESSION_REDIS']=StrictRedis(host=load_dict['redis_ip'], port=6379) 
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes= 30)
Session(app)
CORS(app, supports_credentials=True)

#logging
logging.basicConfig(level=logging.INFO,
                    filename=os.path.join(Root_DIR, 'log/blog.log'),
                    datefmt='%Y/%m/%d %H:%M:%S',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(module)s - %(message)s')
logger = logging.getLogger('blog')

"""自定义异常处理"""
@app.errorhandler(400)
def handle_400_error(error): 
    return jsonify({'code':400,'msg':str(error)})




@app.after_request
def af_request(resp):     
    """
    #请求钩子，在所有的请求发生后执行，加入headers。
    :param resp:
    :return:
    """
    resp = make_response(resp)
    resp.headers['Access-Control-Allow-Origin'] = load_dict['Access-Control-Allow-Origin']
    
    if app.debug== True:
        resp.headers['Access-Control-Allow-Origin'] = request.headers.get('Origin')

    resp.headers['Access-Control-Allow-Methods'] = 'GET,POST'
    resp.headers['Access-Control-Allow-Headers'] = load_dict['Access-Control-Allow-Headers']
    resp.headers['Access-Control-Allow-Credentials'] = 'true'
    resp.headers['Cache-Control'] = 'no-cache'
    return resp

#查询全部人员的博客数
@app.route("/blog/total",methods = ["GET"])
def total():     
    db.session.commit()

        #添加偏移量,之后在前端中加入此字段,应该是offset = request.form['offset']
    offset = 0   
    try:
        data = db.session.query(Blog).offset(offset).limit(10).all()
    except Exception as e:
        logger.info(e,exc_info=True)
        return jsonify({'code':500,'msg':'sqlserver error'})

    resp = {}
    resp['code'] = 0
    resp['msg'] = 'success query'
    resp_data = {}
    resp_data['datacount'] = len(data)
    data_list = []
    for i in data :
        single_data = {}
        single_data['blogid'] = i.blogid
        single_data['author'] = i.author
        single_data['content'] = i.content
        single_data['title'] = i.title
        single_data['comment_num'] = i.comment_num  #后续补上
        single_data['date'] = i.sub_date
        data_list.append(single_data)
    resp_data['data'] = data_list
    resp['data'] = resp_data
    resp['offset'] = offset + len(data)
    return jsonify(resp)

#查询当前用户的博客
@app.route("/blog/user/",methods = ["GET"])
def blogUserQuery():
    if 'username' in session:
        #csrf check
        if request.headers.get('csrfToken') == session['csrf']:
            pass
        else:
            abort(400)  

        userName = session['username']
        
     
        #添加偏移量,之后在前端中加入此字段,应该是offset = request.form['offset']
        offset = 0      
        try:
            db.session.commit()
            data = db.session.query(Blog).filter_by(author = userName).offset(offset).limit(10).all()
        except Exception as e:
            logger.info(e,exc_info=True)
            return jsonify({'code':500,'msg':'sqlserver error'})
        
        resp = {}
        resp['code'] = 0
        resp['msg'] = 'success query'
        resp_data = {}
        resp_data['datacount'] = len(data)
        data_list = []
        for i in data :
            single_data = {}
            single_data['blogid'] = i.blogid
            single_data['author'] = i.author
            single_data['content'] = i.content
            single_data['title'] = i.title
            single_data['comment_num'] = i.comment_num #后续补上
            single_data['date'] = i.sub_date
            data_list.append(single_data)
        resp_data['data'] = data_list
        resp['data'] = resp_data
        resp['offset'] = offset + len(data)

        return jsonify(resp)
       
    else:
        return jsonify({'code':403,'msg':'please log in'})

#修改当前用户的博客
@app.route("/blog/modify/",methods = ["POST"])
def blogModify():
    if 'username' in session: 
        #csrf check
        if request.headers.get('csrfToken')  == session['csrf']:
            pass
        else:
            abort(400)  

        bid = request.form['blogid']
        title  = request.form['title']
        content = request.form['content']
        comment_num = request.form['comment_num']  
        checkInt(bid)
        checkInt(comment_num)
        checkStr(title,40)
        checkStr(content,65535)
        
        origin_data = Blog.query.filter_by(blogid = bid ).first()
        if not origin_data == None:
            if origin_data.author == session['username']:
                try:
                    origin_data.title = title
                    origin_data.content = content
                    origin_data.sub_date = datetime.datetime.now()
                    db.session.commit()
                    return jsonify({'code':0,'msg':'success update'})
                except Exception as e:
                    logger.info(e,exc_info=True)
                    db.session.rollback()
                    return jsonify({'code':500,'msg':'sqlserver error'})
            else:
                return jsonify({'code':404,'msg':"you don't have the power"})
        else:
            return jsonify({'code':405,'msg':"request blog not exist"})

    else:
        return jsonify({'code':403,'msg':'please log in'})

#为当前用户添加一条博客
@app.route("/blog/add/",methods = ["POST"])
def blogAdd():
    if 'username' in session: 
        #csrf check
        if request.headers.get('csrfToken')  == session['csrf']:
            pass
        else:
            abort(400)  
        userName = session['username']
        title = request.form['title']
        content = request.form['content']
        checkStr(title,40)
        checkStr(content,65535)

        try:
            new_data = Blog(title,userName,content)
            db.session.add(new_data)
            db.session.commit()
            return jsonify({'code':0,'msg':'success add'})
        except Exception as e:
            logger.info(e,exc_info=True)
            db.session.rollback()
            return jsonify({'code':500,'msg':'sqlserver error'})
    else:
        return jsonify({'code':403,'msg':'please log in'})

#为当前用户删除一条博客
@app.route("/blog/delete/",methods = ["POST"])
def blogDelete():
    if 'username' in session:
        #csrf check
        if request.headers.get('csrfToken')  == session['csrf']:
            pass
        else:
            abort(400)  

        bid = request.form['blogid']
        checkInt(bid)
        #行锁
        db.session.commit()
        origin_data = db.session.query(Blog).filter(Blog.blogid == bid).with_for_update().first()
        if not origin_data == None:
            if origin_data.author == session['username']:
                try:
                    #删除该博客相关联的评论
                    ref_commentList = BlogComment.query.filter_by(blogid = bid).all()
                    for i in ref_commentList:
                        db.session.delete(i)
                    db.session.delete(origin_data)
                    db.session.commit()
                    return jsonify({'code':0,'msg':'success delete'})
                except Exception as e:
                    logger.info(e,exc_info=True)
                    db.session.rollback()
                    return jsonify({'code':500,'msg':'sqlserver error'})
            else:
                return jsonify({'code':404,'msg':"you don't have the power"})
        else:
            return jsonify({'code':405,'msg':"request blog not exist"})
    else:
        return jsonify({'code':403,'msg':'please log in'})

@app.route("/rank/",methods = ["GET"])
#@trace
def getRank():
    # headers = getForwardHeaders(request)
    headers = request.headers
    try:
        url = load_dict['rank_service_domain']+ "/getRank/" 
        res = requests.get(url, headers=headers, timeout=5.0)
    except:
        res = None
    if res and res.status_code == 200:
        return jsonify(res.json())
    else:
        status = res.status_code if res is not None and res.status_code else 500
        return jsonify({'code':500,'error': 'Sorry, rank service are currently unavailable for you now.'})    

            
if __name__ == '__main__':
    app.run(host = '0.0.0.0' ,port=5555, debug=True)