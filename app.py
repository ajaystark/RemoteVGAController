from flask import Flask, render_template
from flask_socketio import SocketIO, emit


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
    return render_template('hello.html', name="Vasu")

@app.route('/typed')
def typedRender():
    return render_template('typing.html')

if __name__ == "__main__":
    socketio.run(app,host="0.0.0.0",port="5000")


