from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from flask import flash, redirect, render_template, request, session, abort
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app)

@socketio.on('my event')
def test_message(message):
    print(message)

@socketio.on('typed')
def typed(message):
    socketio.emit('typing', data=message['data'])

@app.route('/')
def hello():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('hello.html', name="Vasu")

@app.route('/login', methods=['POST'])
def do_admin_login():
    if request.form['password']=='password' and request.form['username']=='admin':
        session['logged_in']=True
    else:
        flash('Wrong Password!')
    return hello()

@app.route('/typed')
def typedRender():
    return render_template('typing.html')


@app.route('/upload')
def upload_file():
   return render_template('first.html')

@app.route('/save', methods = ['GET', 'POST'])
def function():
	if request.method == 'POST':
		f = request.files['file']
		f.save(f.filename)
		query=f.filename
	return render_template('second.html',query=f.filename)




if __name__ == "__main__":
    app.secret_key=os.urandom(12)
    socketio.run(app,host='0.0.0.0', debug=True)
    #app.run(host='0.0.0.0')

