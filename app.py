from flask import Flask, render_template, flash, redirect, render_template, request, session, abort,send_from_directory, url_for
from flask_socketio import SocketIO, emit
from flask_cors import CORS, cross_origin
from flask_security import Security, login_required, SQLAlchemySessionUserDatastore
from flask_login import LoginManager, login_user, current_user, logout_user
from database import db_session, init_db
from models import User, Role
from forms import *
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = os.urandom(24)

user_datastore = SQLAlchemySessionUserDatastore(db_session, User, Role)

security = Security(app, user_datastore)

app.config['DEFAULT_PARSERS'] = [
    'flask.ext.api.parsers.JSONParser',
    'flask.ext.api.parsers.URLEncodedParser',
    'flask.ext.api.parsers.FormParser',
    'flask.ext.api.parsers.MultiPartParser'
]

@app.before_first_request
def create_db():
    init_db()
    db_session.commit()

UPLOAD_FOLDER = './static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
login_manager = LoginManager()
login_manager.init_app(app)

cors = CORS(app,resources={r"/*":{"origins":"*"}})
socketio = SocketIO(app)

"""
    Socket Methods Start
"""
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

"""
    Socket Methods End
"""


"""
    Auth methods Start
"""

def create_user(email, password, name):
    print('create user called')
    user_datastore.create_user(email=email, password=generate_password_hash(password, method='sha256'), name=name)
    db_session.commit()

@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in on every page load."""
    if user_id is not None:
        print(user_id)
        session['logged_in'] = True
        return User.query.get(user_id)
    return None


"""
    Auth Methods End
"""


"""
    App Routes Start
"""
@app.route('/')
def hello():
    socketio.emit('bringBackTheSlaves')
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('start.html')

@app.route('/hello')
@login_required
def hello1():
    return render_template('hello.html', name="Vasu")

@app.route('/login_user', methods=['POST', 'GET'])
def do_admin_login():
    #print('LOGIN!!!!\n\n')
    if (request.method == 'POST'):
        #print('\n\n\nHERE!\n\n\n')
        password = request.form['password']
        email = request.form['email']
        # if(password==):
        #     flash('Wrong Password!')
        checkUser = User.query.filter_by(email=email).first()
        if checkUser is None:
            flash('This Email ID Doesn\'t exist')
            return redirect(url_for('hello'))
        else:
            if checkUser.check_password(password=password):
                session['logged_in']=True
                current_user = login_user(checkUser)
                #print(request.form['email'], request.form['password'])
                session['name'] = "<<Fix Name Error>> "#current_user.query.get(name)
                session['description'] = request.form['Description']
                return redirect(url_for('hello'))
            else:
                flash('Wrong Password!')
                return redirect(url_for('hello'))
    else:
        flash('Wrong Password!')
        return redirect(url_for('hello'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session['logged_in']=False
    return redirect('/')

@app.route('/createAccount', methods=['GET'])
def createUserAccount():
    return render_template('createAccount.html')

@app.route('/register', methods=['POST', 'GET'])
def do_admin_register():
    if (request.method == 'POST'):
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        existing_user = User.query.filter_by(email=email).first()
        if existing_user is None:
            create_user(email=request.form['email'], password=request.form['password'], name=request.form['name'])
            return redirect(url_for('hello'))
        else:
            flash('Wrong Password!')
            return redirect(url_for('createUserAccount'))
    return redirect(url_for('createUserAccount'))


@app.route('/clientelle')
def clientelle():
    try:
        file=open("name.txt","r")
        temp=file.read()
        return render_template('clientelle.html', query=temp, name=session.get('name'), description=session.get('description'))
    except:
        return render_template('clientelle.html', name=session.get('name'), description=session.get('description'))

@app.route('/typed')
def typedRender():
    return render_template('typing.html')

@app.route('/screen')
def sharescreen():
    socketio.emit('screenClient')
    return render_template('screen.html')

@app.route('/watch')
def watchScreen():
    return render_template('watchScreen.html')

@app.route('/upload')
@login_required
def upload_file():
    socketio.emit('sendClient')
    return render_template('first.html')

@app.route('/slave')
def slave():
    return render_template('slave.html')

@app.route('/clientelle2')
def clientelle2():
    return render_template('clientelle2.html', name=session.get('name'), description=session.get('description'))

@app.route('/save', methods = ['GET', 'POST'])
@login_required
def function():
    if request.method == 'POST':
        f = request.files['file']
        f.save(os.path.join(app.config['UPLOAD_FOLDER'],f.filename))
        file=open("name.txt","w")
        file.write(f.filename)
        file.close()
        socketio.emit('reloadClient', data= f.filename)
    return render_template("first.html")


@app.route("/client")
def client():
    file=open("name.txt","r")
    temp=file.read()
    return render_template("second.html",query=temp)

"""
    App Routes End
"""

if __name__ == "__main__":
    app.secret_key=os.urandom(12)
    socketio.run(app,host='0.0.0.0', debug=True)