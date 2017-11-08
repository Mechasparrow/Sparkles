from flask import Flask
from flask_sockets import Sockets

import os

app = Flask(__name__)
sockets = Sockets(app)

miners = []
nodes = []

try:
    port = int(os.environ["PORT"])
except KeyError:
    port = 5000

@sockets.route('/miners')
def miners_socket(ws):
    while not ws.closed:
        break

@sockets.route('/wallet')
def wallet_socket(ws):
    while not ws.closed:
        ws.send("terminate")


if __name__ == "__main__":
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler

    print ("running server on port " + str(port))
    server = pywsgi.WSGIServer(('', port), app, handler_class=WebSocketHandler)
    server.serve_forever()
