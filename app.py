from flask import Flask, render_template
from flask_socketio import SocketIO, emit

from flask_cors import CORS, cross_origin


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

app.config['DEFAULT_PARSERS'] = [
    'flask.ext.api.parsers.JSONParser',
    'flask.ext.api.parsers.URLEncodedParser',
    'flask.ext.api.parsers.FormParser',
    'flask.ext.api.parsers.MultiPartParser'
]
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
    return render_template('hello.html', name="Vasu")

@app.route('/typed')
def typedRender():
    return render_template('typing.html')

@app.route('/screen')
def sharescreen():
    return render_template('screen.html')

@app.route('/watch')
def watchScreen():
    return render_template('watchScreen.html')

if __name__ == "__main__":
    socketio.run(app,host="0.0.0.0",port="5000", debug=True)


