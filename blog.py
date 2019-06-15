from UserModel import User,Blog,db
from flask import Flask,request,jsonify,session
from flask_session import Session
from redis import StrictRedis
from datetime import timedelta
import hashlib

app=Flask(__name__)
app.config['SESSION_TYPE']='redis'
app.config['SESSION_REDIS']=StrictRedis(host='115.159.182.126', port=6379) 
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes = 30)
Session(app)

@app.route("/blog/total",methods = ["GET"])
def total():
    if 'username' in session:
        userName = session['username']       
        data = Blog.query.filter_by(author = userName).all()
        resp = {}
        resp['code'] = 200
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
            single_data['comment_num'] = 0  #后续补上
            single_data['date'] = i.sub_date
            data_list.append(single_data)
        resp_data['data'] = data_list
        resp['data'] = resp_data

        return jsonify(resp)
    else:
        return jsonify({'code':403,'msg':'please log in'})

@app.route("/blog/user",methods = ["GET"])
def blogUserQuery():
    if 'username' in session:
        userName = session['username']       
        data = Blog.query.all()
        resp = {}
        resp['code'] = 200
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
            single_data['comment_num'] = 0 #后续补上
            single_data['date'] = i.sub_date
            data_list.append(single_data)
        resp_data['data'] = data_list
        resp['data'] = resp_data

        return jsonify(resp)
    else:
        return jsonify({'code':403,'msg':'please log in'})


if __name__ == '__main__':
    app.run(port=6000, debug=True)