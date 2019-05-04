from flask import Flask, render_template, flash, redirect, render_template, request, session, abort,send_from_directory
from flask_socketio import SocketIO, emit
from flask_cors import CORS, cross_origin
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

app.config['DEFAULT_PARSERS'] = [
    'flask.ext.api.parsers.JSONParser',
    'flask.ext.api.parsers.URLEncodedParser',
    'flask.ext.api.parsers.FormParser',
    'flask.ext.api.parsers.MultiPartParser'
]


UPLOAD_FOLDER = '/Users/ajay/vga/static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



cors = CORS(app,resources={r"/*":{"origins":"*"}})
socketio = SocketIO(app)

@socketio.on('my event')
def test_message(message):
    print(message)

@socketio.on('typed')
def typed(message):
    socketio.emit('typing', data=message['data'])

@socketio.on('videoFromServer')
def videoFromServer(message):
    #print("Here: " + message['data'])
    socketio.emit('displayVid', data=message['data'])

@app.route('/')
def hello():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('start.html')

@app.route('/hello')
def hello1():
    return render_template('hello.html', name="Vasu")

@app.route('/login', methods=['POST'])
def do_admin_login():
    if request.form['password']=='password' and request.form['username']=='admin':
        session['logged_in']=True
    else:
        flash('Wrong Password!')
    return hello()

@app.route('/clientelle')
def clientelle():
    return render_template('clientelle.html')

@app.route('/typed')
def typedRender():
    return render_template('typing.html')

@app.route('/screen')
def sharescreen():
    return render_template('screen.html')

@app.route('/watch')
def watchScreen():
    return render_template('watchScreen.html')

@app.route('/upload')
def upload_file():
   return render_template('first.html')


UPLOAD_FOLDER = '/home/skullcrush3rx/Desktop/RemoteVGAController/static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/save', methods = ['GET', 'POST'])
def function():
    if request.method == 'POST':
        f = request.files['file']
        f.save(os.path.join(app.config['UPLOAD_FOLDER'],f.filename))
        

        file=open("name.txt","w")
        file.write(f.filename)
        file.close()
    return render_template("first.html")


@app.route("/client")
def client():
    file=open("name.txt","r")
    temp=file.read()
    # return send_from_directory(app.config['UPLOAD_FOLDER'],filename=temp)
    return render_template("second.html",query=temp)


if __name__ == "__main__":
    app.secret_key=os.urandom(12)
    socketio.run(app,host='0.0.0.0', debug=True)
    #app.run(host='0.0.0.0')


