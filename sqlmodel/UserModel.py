# coding=utf-8
import os 
import sys
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) #该执行模块所在文件夹的父文件夹
Root_DIR = os.path.dirname(BASE_DIR) #该执行模块文件夹的父文件夹即项目根目录
sys.path.append(Root_DIR)
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime
import json


#读取配置
with open(os.path.join(Root_DIR, "config.json"),'r') as load_f:
    load_dict = json.load(load_f)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = load_dict['mysql']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =True
db = SQLAlchemy(app)



#创建User模型
class User(db.Model):
    __tablename__ = 'User' #起表名
    username = db.Column(db.String(25),primary_key=True)
    passwd = db.Column(db.String(40),nullable = False)

    def __init__(self,username,passwd):
        self.username = username
        self.passwd = passwd

#创建博客内容模型
class Blog(db.Model):
    __tablename__ = 'Blog'
    blogid = db.Column(db.Integer , primary_key = True, nullable = False)
    title = db.Column(db.String(40),nullable = False)
    author = db.Column(db.String(25),nullable = False)
    content = db.Column(db.Text,nullable = False)
    sub_date = db.Column(db.DateTime,default = datetime.datetime.now())
    comment_num = db.Column(db.Integer)

    def __init__(self, title , author , content,comment_num = 0):
        self.title = title
        self.author = author
        self.content = content
        self.comment_num = 0

#创建博客评论模型
class BlogComment(db.Model):
    __tablename__ = 'BlogComment'
    commentid = db.Column(db.Integer , primary_key = True, nullable = False)
    blogid = db.Column(db.Integer , nullable = False)
    author = db.Column(db.String(25),nullable = False)
    content = db.Column(db.Text,nullable = False)
    sub_date = db.Column(db.DateTime,default = datetime.datetime.now())

    def __init__(self,blogid, author , content):
        self.blogid = blogid
        self.author = author
        self.content = content

