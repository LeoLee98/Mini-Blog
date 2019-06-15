from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:mysql199806@115.159.182.126/Blog'
db = SQLAlchemy(app)

#创建User模型
class User(db.Model):
    __tablename__ = 'User' #起表名
    username = db.Column(db.String(25),primary_key=True)
    passwd = db.Column(db.String(40),nullable = False)

    def __init__(self,username,passwd):
        self.username = username
        self.passwd = passwd

