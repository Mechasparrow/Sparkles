from flask import Flask
from flask_sockets import Sockets

import os
import json

import copy

app = Flask(__name__)
sockets = Sockets(app)

miners = []
nodes = []

need_sync = []

try:
    port = int(os.environ["PORT"])
except KeyError:
    port = 5000

@sockets.route('/miners')
def miners_socket(ws):
    global need_sync
    while not ws.closed:
        data = ws.receive()

        try:
            data_decoded = json.loads(data)
        except TypeError:
            if (ws in miners):
                miners.remove(ws)

            if (ws in nodes):
                nodes.remove(ws)

            print (str(len(miners)) + " active miners")
            break;

        if (data_decoded['message_type'] == 'connection'):
            if (data_decoded['connection'] == True):
                miners.append(ws)
                nodes.append(ws)
                print (str(len(miners)) + " active miners")
            elif (data_decoded['connection'] == False):
                miners.remove(ws)
                nodes.remove(ws)
                print (str(len(miners)) + " active miners")
        elif(data_decoded['message_type'] == 'new_block'):
            print ('new block!')

            for node in nodes:
                node.send(data)

        elif (data_decoded['message_type'] == "sync"):

            sync_message = {
                'message_type': 'sync_request',
            }

            sync_message_json = json.dumps(sync_message)

            need_sync.append(ws)

            for node in nodes:
                if (node == ws):
                    continue

                node.send(sync_message_json)

        elif(data_decoded['message_type'] == 'blockchain_upload'):
            print ("blockchain sync")

            blockchain = data_decoded['blockchain']

            print ("miner sent...")
            print (blockchain)

            need_sync_old = copy.copy(need_sync)

            for node in need_sync_old:
                if (node == ws):
                    print ("same node")
                else:
                    node.send(data)
                    need_sync.remove(node)

            print (need_sync)



@sockets.route('/wallet')
def wallet_socket(ws):
    global need_sync
    while not ws.closed:
        data = ws.receive()

        try:
            data_decoded = json.loads(data)
        except TypeError:
            print ("node disconnected")

            if ws in nodes:
                nodes.remove(ws)

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
        elif (data_decoded['message_type'] == "sync"):

            sync_message = {
                'message_type': 'sync_request',
            }

            sync_message_json = json.dumps(sync_message)

            need_sync.append(ws)

            for node in nodes:
                if (node == ws):
                    continue

                node.send(sync_message_json)

        elif (data_decoded['message_type'] == "blockchain_upload"):
            print ("blockchain sync")

            blockchain = data_decoded['blockchain']
            print ("node sent...")
            print (blockchain)


            need_sync_old = copy.copy(need_sync)

            for node in need_sync_old:
                if (node == ws):
                    print ("same node")
                else:
                    node.send(data)
                    need_sync.remove(node)

            print (need_sync)

if __name__ == "__main__":
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler

    print ("running server on port " + str(port))
    server = pywsgi.WSGIServer(('', port), app, handler_class=WebSocketHandler)
    server.serve_forever()
