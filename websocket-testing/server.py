from flask import Flask
from flask_sockets import Sockets

app = Flask(__name__)
sockets = Sockets(app)

miners = []

@sockets.route('/miners')
def miners_socket(ws):
    while not ws.closed:
        message = ws.receive()
        print (message)
        ws.send(message)

@sockets.route('/wallet')
def wallet_socket(ws):
    while not ws.closed:
        message = ws.receive()
        print (message)
        ws.send(message)

if __name__ == "__main__":
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
    server.serve_forever()
