import threading

import socket
import json

from peer_broadcast import PeerBroadcast

BUFFER_SIZE = 1024

## Utility peer sync
def merge_peer_list(old_peer_list, new_peer_list, server_ip, server_port):

    ## Remove self from list

    self_info = {
        "address": server_ip,
        "port": server_port
    }

    ## Merge old list and new list

    raw_peer_list = old_peer_list + new_peer_list

    ## Delete ref to self

    if self_info in raw_peer_list:
        raw_peer_list.remove(self_info)

    ## Remove duplicates

    merged_peer_list = []

    seen = set()
    for peer_info in raw_peer_list:
        t = tuple(peer_info.items())
        if t not in seen:
            seen.add(t)
            merged_peer_list.append(peer_info)

    return merged_peer_list

class PeerListRetrieval(threading.Thread):

    def __init__(self, peer, peer_list, server_ip, server_port):
        threading.Thread.__init__(self)
        self.peer = peer
        self.peer_list = peer_list
        self.server_ip = server_ip
        self.server_port = server_port

    def run(self):
        peer = self.peer

        PEER_IP = peer["address"]
        PORT = peer["port"]

        peer_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        peer_conn.settimeout(2.0)
        peer_conn.connect((peer["address"], peer["port"]))

        peer_info_json = {
            "message_type": "peer_list"
        }

        peer_info_string = json.dumps(peer_info_json)

        try:

            try:

                peer_conn.sendall(peer_info_string.encode('utf-8'))

                response_data = peer_conn.recv(BUFFER_SIZE).decode('utf-8')

                response_data_json = json.loads(response_data)
                if (response_data_json["message_type"] == "peer_list"):

                    new_peer_list = response_data_json["peer_list"]

                    global PEER_LIST
                    NEW_PEER_LIST = merge_peer_list(self.peer_list, new_peer_list, self.server_ip, self.server_port)

                    print ()
                    print ("NEW LIST: " + str(NEW_PEER_LIST))


                    self.peer_list = NEW_PEER_LIST

                else:
                    print ("PEER FAILURE")

                peer_conn.close()
                return

            except socket.timeout:
                print ("unable to send peer info")
                return
        except ConnectionRefusedError:
            print ("connection refused")

class SendServerInfo(threading.Thread):

    def __init__(self, peer, server_ip, server_port):
        threading.Thread.__init__(self)
        self.peer = peer
        self.server_ip = server_ip
        self.server_port = server_port

    def run(self):
        peer = self.peer

        PEER_IP = peer["address"]
        PORT = peer["port"]

        peer_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        peer_conn.settimeout(2.0)
        peer_conn.connect((peer["address"], peer["port"]))

        peer_info_json = {
            "message_type": "peer_info",
            "content": {
                "ip": self.server_ip,
                "port": self.server_port
            }
        }

        peer_info_string = json.dumps(peer_info_json)

        try:

            try:

                peer_conn.sendall(peer_info_string.encode('utf-8'))

                response_data = peer_conn.recv(BUFFER_SIZE).decode('utf-8')
                response_data_json = json.loads(response_data)

                if (response_data_json["message_type"] == "success"):
                    print ("PEER SUCCESS")
                else:
                    print ("PEER FAILURE")

                peer_conn.close()
                return

            except socket.timeout:
                print ("unable to send peer info")
                return
        except ConnectionRefusedError:
            print ("connection refused")



class Client_P2P(threading.Thread):

    def __init__(self, peer_list, server, client_code):
        threading.Thread.__init__(self)
        self.peer_list = peer_list
        self.server_ip = server.server_ip
        self.server_port = server.server_port
        self.client_code = client_code

    def send_message(self, message):
        node_info = {
            "address": self.server_ip,
            "port": self.server_port
        }

        for peer in self.peer_list:
            broadcast_message_thread = PeerBroadcast(peer, message, self.peer_list, node_info)
            broadcast_message_thread.start()

    def send_peer_info(self):

        for peer in self.peer_list:
            print (peer)

            peer_info_thread = SendServerInfo(peer, self.server_ip, self.server_port)
            peer_info_thread.start()

    def sync_peer_list(self):

        list_threads = []

        for peer in self.peer_list:

            peer_list_thread = PeerListRetrieval(peer, self.peer_list, self.server_ip, self.server_port)
            peer_list_thread.start()
            list_threads.append(peer_list_thread)

        for list_thread in list_threads:
            list_thread.join()

    def run(self):
        print ("client code")

        # Send server information to fellow est peers

        self.send_peer_info()

        # sync peer list

        self.sync_peer_list()


        print ()
        print ("FINAL: " + str(self.peer_list))

        # Software loop
        self.client_code(self.send_message)
