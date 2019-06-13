import mysql.connector
from flask import Flask 

app = Flask(__name__)
db = mysql.connector.connect(user='root', password ='mysql199806', database='Blog',host = '115.159.182.126')

#sql = 'select * from BlogComment'
#sql = 'insert into BlogComment(blogid,author,content,sub_date) values(1,"test2","test2","2019-06-15 19:47:44")'
sql = 'select * from BlogComment order by sub_date desc'
cursor = db.cursor()

@app.route('/',methods=["GET","POST"])
def getComment():
    try:
    # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行,查询不用commit
        # db.commit()
        print(jsonify(cursor.fetchall()[0]))
        return jsonify(cursor.fetchall()[0])
    except:
        # Rollback in case there is any error
        print("error and rollback")
        #db.rollback()

if __name__ == '__main__':
    app.run(port = 5000 , debug = True)

#print(cursor.fetchall())