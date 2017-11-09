from flask import Flask
from flask_sockets import Sockets

import os
import json

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
        data = ws.receive()

        try:
            data_decoded = json.loads(data)
        except TypeError:
            miners.remove(ws)
            print (str(len(miners)) + " active miners")
            break;

        if (data_decoded['message_type'] == 'connection'):
            if (data_decoded['connection'] == True):
                miners.append(ws)
                print (str(len(miners)) + " active miners")
            elif (data_decoded['connection'] == False):
                miners.remove(ws)
                print (str(len(miners)) + " active miners")


@sockets.route('/wallet')
def wallet_socket(ws):
    while not ws.closed:
        message = ws.receive()
        message_decoded = json.loads(message)
        print (message)

        if (message == "wallet connect"):
            nodes.append(ws)
        elif (message == "wallet disconnect"):
            nodes.remove(ws)
        elif (message == "get nodes"):
            ws.send(str(len(nodes)))
        elif (message_decoded['message_type'] == "transaction"):
            print ("transaction")

if __name__ == "__main__":
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler

    print ("running server on port " + str(port))
    server = pywsgi.WSGIServer(('', port), app, handler_class=WebSocketHandler)
    server.serve_forever()
