from flask import Flask,session,request

from flask_session import Session
from redis import StrictRedis

app=Flask(__name__)

app.config['DEBUG']=True
app.config['SESSION_TYPE']='redis'
app.config['SESSION_REDIS']=StrictRedis(host='115.159.182.126', port=6379)    
Session(app)    

@app.route("/set/<arg>") 
def set(arg):
    print (request)
    session['key']=arg
    return 'save session'

@app.route("/set2/<arg>") 
def set2(arg):
    print (request)
    session['set2']=arg
    return 'save session'
    

@app.route("/get/")
def get():
    if not 'key' in session:
        return 'please login'
    return session.get('key','not set')

@app.route("/get2/")
def get2():
    if not 'set2' in session:
        return 'please login'
    return session.get('set2','not set')



@app.route("/delete/")
def delete():
    if 'key' in session :     
        print (session.get('key','not set'))
        session.pop('key')
        return 'success delete'
    else:
        return 'please login'

if __name__=="__main__":
    app.run(port = 5555,debug=app.config['DEBUG'])