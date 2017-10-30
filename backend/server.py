from flask import Flask, render_template
from flask_socketio import SocketIO

from flask_socketio import send, emit

app = Flask(__name__)
socketio = SocketIO(app)

@socketio.on('message')
def handle_message(message):
    print(message)
    emit('message_response', {'data': 'got message'})

if __name__ == '__main__':
    socketio.run(app)
