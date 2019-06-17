# coding=utf-8
import sys
sys.path.append("..")
from sqlmodel.UserModel import User,Blog,BlogComment,db
from flask import Flask,request,jsonify,session,make_response
from flask_session import Session
from redis import StrictRedis
from datetime import timedelta
from flask_cors import CORS
import hashlib
import logging

app=Flask(__name__)
app.config['SESSION_TYPE']='redis'
app.config['SESSION_REDIS']=StrictRedis(host='115.159.182.126', port=6379) 
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes = 30)
Session(app)
CORS(app, supports_credentials=True)

#输出到文件
logging.basicConfig(level=logging.INFO,
                    filename='rank.log',
                    datefmt='%Y/%m/%d %H:%M:%S',
                    format='%(asctime)s - %(levelname)s - %(lineno)d - %(module)s - %(message)s')
logger = logging.getLogger('rank')

#debug on the console
# console = logging.StreamHandler()
# console.setLevel(logging.WARNING)
# formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
# console.setFormatter(formatter)

# logging.getLogger('').addHandler(console)

@app.after_request
def af_request(resp):     
    """
    #请求钩子，在所有的请求发生后执行，加入headers。
    :param resp:
    :return:
    """
    resp = make_response(resp)
    resp.headers['Access-Control-Allow-Origin'] = 'http://115.236.123.247:8090'
    resp.headers['Access-Control-Allow-Methods'] = 'GET,POST'
    resp.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type,end-user'
    resp.headers['Access-Control-Allow-Credentials'] = 'true'
    return resp

#按照评论数排序
@app.route("/rank/",methods=['GET'])
def rankComment():
    try:
        data = Blog.query.order_by(Blog.comment_num).all()
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
            single_data['title'] = i.title
            single_data['comment_num'] = i.comment_num  #后续补上
            single_data['date'] = i.sub_date
            data_list.append(single_data)
        resp_data['data'] = data_list
        resp['data'] = resp_data

        return jsonify(resp)
    except Exception as e:
        logger.info(e,exc_info=True)
        return jsonify({'code':500,'msg':'sqlserver error'}) 


#按照日期排序
@app.route("/rank/date/",methods=['GET'])
def rankDate():
    try:
        data = Blog.query.order_by(Blog.sub_date).all()
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
            single_data['title'] = i.title
            single_data['comment_num'] = i.comment_num  #后续补上
            single_data['date'] = i.sub_date
            data_list.append(single_data)
        resp_data['data'] = data_list
        resp['data'] = resp_data

        return jsonify(resp)
    except Exception as e:
        logger.info(e,exc_info=True)
        return jsonify({'code':500,'msg':'sqlserver error'}) 

if __name__ == '__main__':
    app.run(debug = True,port = 7777)