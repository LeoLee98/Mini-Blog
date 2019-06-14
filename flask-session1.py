from flask import Flask,session

from flask_session import Session
from redis import StrictRedis

app=Flask(__name__)

app.config['DEBUG']=True
app.config['SESSION_TYPE']='redis'
app.config['SESSION_REDIS']=StrictRedis(host='115.159.182.126', port=6379)    
Session(app)    

@app.route("/set/") 
def set():
    session['key']='value'
    return 'save session'

@app.route("/get/")
def get():
    return session.get('key','not set')
    
if __name__=="__main__":
    app.run(debug=app.config['DEBUG'])