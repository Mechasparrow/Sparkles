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
            if (ws in miners):
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
        data = ws.receive()

        try:
            data_decoded = json.loads(data)
        except TypeError:
            print ("node disconnected")
            break;

        if (data_decoded['message_type'] == "connection"):
            if (data_decoded['connection'] == True):
                nodes.append(ws)
                print ("node connected")
            elif (data_decoded['connection'] == False):
                nodes.remove(ws)
                print ("node disconnected")
        elif (data_decoded['message_type'] == "transaction"):
            for miner in miners:
                miner.send(data)

        elif (data_decoded['message_type'] == "command"):
            if (data_decoded['command'] == "get_nodes"):

                message_response = {
                    'message_type': 'message',
                    'message': 'There is ' + str(len(nodes)) + ' nodes connected.'
                }

                message_response_json = json.dumps(message_response)

                ws.send(message_response_json)

if __name__ == "__main__":
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler

    print ("running server on port " + str(port))
    server = pywsgi.WSGIServer(('', port), app, handler_class=WebSocketHandler)
    server.serve_forever()
