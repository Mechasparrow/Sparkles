from flask import Flask
from flask_sockets import Sockets

import os


app = Flask(__name__)
sockets = Sockets(app)

try:
    port = int(os.environ["PORT"])
except KeyError:
    port = 5000

print(port)

@sockets.route('/echo')
def echo_socket(ws):
    while not ws.closed:
        message = ws.receive()
        ws.send(message)


@app.route('/')
def hello():
    return 'Hello World!'


if __name__ == "__main__":
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(('', port), app, handler_class=WebSocketHandler)
    server.serve_forever()
