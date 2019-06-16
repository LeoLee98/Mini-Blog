from flask import Flask, redirect, url_for, request,render_template,make_response,session, escape
app = Flask(__name__)
    
@app.route('/success/<name>')
def success(name):
    userid = request.cookies.get('user')
    if not userid == None:
        return 'Welcome %s' %name
    else:
        return redirect(url_for('index'))

@app.route('/welcome',methods=['GET','POST'])
def welcome():
    userid = request.cookies.get('user')
    if not userid == None:
        if request.method == 'POST':
            return redirect(url_for('success',name = userid))
        else:
            return render_template('welcome.html')
    return redirect(url_for('index'))

@app.route('/login',methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        pwd = request.form['passwd']
        print(user,pwd)
        resp = make_response(redirect(url_for('welcome')))
        resp.set_cookie('user',user)
        return resp
    return render_template('login.html')

# @app.route('/regist',methods = ['POST'])
# def regist():
    
@app.route('/')
def index():
   return render_template('index.html')

@app.route('/A',methods=['GET','POST'])
def testSession():
    if 'username' in session:
        return 'Logged in A as %s' % escape(session['username'])
    return 'You are not logged in A'

# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == '__main__':
   app.run(port = 5000, debug = True)