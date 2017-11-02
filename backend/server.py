from flask import Flask, render_template
from flask_socketio import SocketIO

from flask_socketio import send, emit
import json

app = Flask(__name__)
socketio = SocketIO(app)

@socketio.on('message')
def handle_message(message):
    print(message)
    emit('message_response', {'data': 'got message'})

@socketio.on('transaction')
def handle_transaction(transaction):
    emit('transaction_response', transaction, broadcast = True)

if __name__ == '__main__':
    socketio.run(app)
