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
    resp.headers['Access-Control-Allow-Origin'] = 'http://115.236.123.247:8090'
    resp.headers['Access-Control-Allow-Methods'] = 'GET,POST'
    resp.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return resp

#搜索某条博客的全部评论
@app.route("/comment/search/",methods = ["POST"])
def commentQuery():   
        bid = request.form['blogid']
        data = BlogComment.query.filter_by(blogid = bid).all()
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

        return jsonify(resp)

#为当前用户新增一条评论
@app.route("/comment/add/",methods = ["POST"])
def commentAdd():
    print(request)
    if 'username' in session: 
        userName = session['username']
        bid = request.form['blogid']
        content = request.form['content']
        ref_blog = Blog.query.filter_by(blogid = bid).first()
        if not ref_blog == None:
            try:
                new_data = BlogComment(bid,userName,content)
                ref_blog.comment_num = ref_blog.comment_num + 1
                db.session.add(new_data)
                db.session.commit()
                return jsonify({'code':0,'msg':'success add'})
            except Exception as e:
                raise e
                return jsonify({'code':500,'msg':'sqlserver error'})
        else:
            return jsonify({'code':405,'msg':"request blog not exist"})
    else:
        return jsonify({'code':403,'msg':'please log in'})




if __name__ == '__main__':
    app.run(port=6666, debug=True)