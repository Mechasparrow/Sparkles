import socket

import threading

import json

import copy

BUFFER_SIZE = 1024

class PeerBroadcast(threading.Thread):

    def __init__(self, peer, message, broadcast_list, node_info):
        threading.Thread.__init__(self)
        self.peer = peer
        self.message = message
        self.broadcast_list = broadcast_list
        self.node_info = node_info

    def run(self):
        print ("broadcasting message")

        peer = self.peer
        message = self.message
        broadcast_list = self.broadcast_list
        node_info = self.node_info


        PEER_IP = peer["address"]
        PORT = peer["port"]

        peer_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        peer_conn.settimeout(2.0)

        try:
            peer_conn.connect((peer["address"], peer["port"]))
        except ConnectionRefusedError:
            print ("peer not online")

            print (peer["address"])
            print (peer["port"])

            return

        new_broadcast_list = copy.copy(broadcast_list)
        new_broadcast_list.append(node_info)

        broadcast_json = {
            "message_type": "broadcast",
            "message": message,
            "broadcast_sent_to": new_broadcast_list
        }

        broadcast_string = json.dumps(broadcast_json)

        try:

            try:

                peer_conn.send(broadcast_string.encode('utf-8'))

                response_data = peer_conn.recv(BUFFER_SIZE).decode('utf-8')

                response_data_json = json.loads(response_data)

                if (response_data_json["message_type"] == "success"):

                    print ("BROADCAST SUCCESS")

                else:
                    print ("BROADCAST FAILURE")

                peer_conn.close()
                return

            except Exception as err:
                print ("unable to send broadcast")
                return
        except ConnectionRefusedError:
            print ("connection refused")
