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
import hashlib
import logging
import json
import time


#读取配置
with open(os.path.join(Root_DIR, "config.json"),'r') as load_f:
    load_dict = json.load(load_f)

app=Flask(__name__)
app.config['SESSION_TYPE']='redis'
app.config['SESSION_REDIS']=StrictRedis(host=load_dict['redis_ip'], port=6379) 
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes = 30)
Session(app)
CORS(app, supports_credentials=True)

logging.basicConfig(level=logging.INFO,
                    filename=os.path.join(Root_DIR, 'log/comment.log'),
                    datefmt='%Y/%m/%d %H:%M:%S',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(module)s - %(message)s')
logger = logging.getLogger('comment')

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

#搜索某条博客的全部评论
@app.route("/comment/search/",methods = ["POST"])
def commentQuery():   
        bid = request.form['blogid']
        checkInt(bid)
        #添加偏移量,之后在前端中加入此字段,应该是offset = request.form['offset']
        offset = 0
        try:
            db.session.commit()
            ref_blog = Blog.query.filter_by(blogid = bid).first()
            if not ref_blog == None:
                try:
                    db.session.commit()
                    data = BlogComment.query.filter_by(blogid = bid).offset(offset).limit(10).all()
                    resp = {}
                    resp['code'] = 0
                    resp['msg'] = 'success query'
                    resp_data = {}
                    resp_data['datacount'] = len(data)

                    data_list = []
                    for i in data :
                        single_data = {}
                        single_data['blogid'] = i.blogid
                        single_data['commentid'] = i.commentid
                        single_data['content'] = i.content
                        single_data['author'] = i.author
                        single_data['date'] = i.sub_date
                        data_list.append(single_data)
                    resp_data['data'] = data_list
                    resp['data'] = resp_data
                    resp['offset'] = offset + len(data)

                    return jsonify(resp)
                except Exception as e:
                    logger.info(e,exc_info=True)
                    return jsonify({'code':500,'msg':'sqlserver error'}) 
            else:
                return jsonify({'code':405,'msg':"request blog not exist"})    
        except Exception as e:
            logger.info(e,exc_info=True)
            return jsonify({'code':500,'msg':'sqlserver error'}) 
        

#为当前用户新增一条评论
@app.route("/comment/add/",methods = ["POST"])
def commentAdd():
    print(request)
    if 'username' in session: 
        #csrf check
        if request.form['token'] == session['csrf']:
            pass
        else:
            abort(400)

        userName = session['username']
        bid = request.form['blogid']
        content = request.form['content']
        checkInt(bid)
        checkStr(content,65535)
        db.session.commit()
        ref_blog = db.session.query(Blog).filter(Blog.blogid == bid).with_for_update().first()
        print(ref_blog)
        if not ref_blog == None:
            try:
                new_data = BlogComment(bid,userName,content)
                ref_blog.comment_num = ref_blog.comment_num + 1
                db.session.add(new_data)
                db.session.commit()
                return jsonify({'code':0,'msg':'success add'})
            except Exception as e:
                logger.info(e,exc_info=True)
                db.session.rollback()
                return jsonify({'code':500,'msg':'sqlserver error'})
        else:
            return jsonify({'code':405,'msg':"request blog not exist"})
    else:
        return jsonify({'code':403,'msg':'please log in'})




if __name__ == '__main__':
    app.run(host = '0.0.0.0', port=6666, debug=True)