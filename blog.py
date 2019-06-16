from UserModel import User,Blog,BlogComment,db
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

#查询全部人员的博客数
@app.route("/blog/total/",methods = ["GET"])
def total():     
        data = Blog.query.filter_by().all()
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
            single_data['comment_num'] = i.comment_num  #后续补上
            single_data['date'] = i.sub_date
            data_list.append(single_data)
        resp_data['data'] = data_list
        resp['data'] = resp_data

        return jsonify(resp)

#查询当前用户的博客
@app.route("/blog/user/",methods = ["GET"])
def blogUserQuery():
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
            single_data['comment_num'] = i.comment_num #后续补上
            single_data['date'] = i.sub_date
            data_list.append(single_data)
        resp_data['data'] = data_list
        resp['data'] = resp_data

        return jsonify(resp)
    else:
        return jsonify({'code':403,'msg':'please log in'})

#修改当前用户的博客
@app.route("/blog/modify/",methods = ["POST"])
def blogModify():
    if 'username' in session: 
        bid = request.form['blogid']
        title  = request.form['title']
        content = request.form['content']
        comment_num = request.form['comment_num']  #可以去除
        
        origin_data = Blog.query.filter_by(blogid = bid ).first()
        if not origin_data == None:
            if origin_data.author == session['username']:
                try:
                    origin_data.title = title
                    origin_data.content = content
                    db.session.commit()
                    return jsonify({'code':200,'msg':'success update'})
                except Exception as e:
                    raise e
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
        userName = session['username']
        title = request.form['title']
        content = request.form['content']
        try:
            new_data = Blog(title,userName,content)
            db.session.add(new_data)
            db.session.commit()
            return jsonify({'code':200,'msg':'success add'})
        except Exception as e:
            raise e
            return jsonify({'code':500,'msg':'sqlserver error'})
    else:
        return jsonify({'code':403,'msg':'please log in'})

#为当前用户删除一条博客
@app.route("/blog/delete/",methods = ["POST"])
def blogDelete():
    if 'username' in session: 
        bid = request.form['blogid']
        origin_data = Blog.query.filter_by(blogid = bid).first()
        if not origin_data == None:
            if origin_data.author == session['username']:
                try:
                    #删除该博客相关联的评论
                    ref_commentList = BlogComment.query.filter_by(blogid = bid).all()
                    for i in ref_commentList:
                        db.session.delete(i)
                    db.session.delete(origin_data)
                    db.session.commit()
                    return jsonify({'code':200,'msg':'success delete'})
                except Exception as e:
                    raise e
                    return jsonify({'code':500,'msg':'sqlserver error'})
            else:
                return jsonify({'code':404,'msg':"you don't have the power"})
        else:
            return jsonify({'code':405,'msg':"request blog not exist"})
    else:
        return jsonify({'code':403,'msg':'please log in'})

            
if __name__ == '__main__':
    app.run(port=5555, debug=True)