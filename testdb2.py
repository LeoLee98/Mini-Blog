import mysql.connector
from flask import Flask 
import json 
app = Flask(__name__)
db = mysql.connector.connect(user='root', password ='mysql199806', database='Blog',host = '115.159.182.126')

#sql = 'select * from BlogComment'
#sql = 'insert into BlogComment(blogid,author,content,sub_date) values(1,"test2","test2","2019-06-15 19:47:44")'
sql = 'select blogid,content from BlogComment order by sub_date desc'
cursor = db.cursor()

# import json

# data = ((2737, 'check_ethstatus'), 
#         (250,'check_ethstatus' ))

# json = json.dumps(dict(data))
# print (json)

try:
# 执行sql语句
    cursor.execute(sql)
        # 提交到数据库执行,查询不用commit
        # db.commit()
    result = cursor.fetchall()
    print(result)
    print(json.dumps(dict(result)))
    # /print(jsonify(cursor.fetchall()[0]))
    #return jsonify(cursor.fetchall()[0])
except BaseException as e:
        # Rollback in case there is any error
    print("error and rollback",e)
    db.rollback()



#print(cursor.fetchall())