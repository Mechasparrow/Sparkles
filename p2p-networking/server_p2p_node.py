import threading

import socket
import json

from peer_broadcast import PeerBroadcast

BUFFER_SIZE = 1024

# The handler for peer connections
class PeerHandler(threading.Thread):

    def __init__(self, conn, peer_list, server):
        threading.Thread.__init__(self)
        self.conn = conn
        self.peer_list = peer_list
        self.server = server

    def run(self):

        print ("handling connection...")

        conn = self.conn

        while True:

            try:
                data = conn.recv(BUFFER_SIZE)

                if not data:
                    break

                decoded_data = data.decode("utf-8")
                decoded_data_json = json.loads(decoded_data)

                print (decoded_data_json)

                if (decoded_data_json["message_type"] == "est_conn"):
                    verify_response = "SPARKLENODE"
                    print ("peer connected!")
                    conn.send(verify_response.encode('utf-8'))
                elif (decoded_data_json["message_type"] == "peer_info"):

                    peer_info = decoded_data_json["content"]

                    actual_peer_info = {
                        "address": peer_info['ip'],
                        "port": peer_info['port']
                    }

                    print (actual_peer_info)

                    self.peer_list.append(actual_peer_info)

                    print (self.peer_list)

                    response_json = {"message_type": "success"}
                    response_json_string = json.dumps(response_json)

                    conn.send(response_json_string.encode('utf-8'))
                elif (decoded_data_json["message_type"] == "peer_list"):

                    peer_list_json = {
                        "message_type": "peer_list",
                        "peer_list": self.peer_list
                    }

                    peer_list_json_string = json.dumps(peer_list_json)

                    conn.send(peer_list_json_string.encode('utf-8'))
                elif (decoded_data_json["message_type"] == "broadcast"):

                    response_json = {"message_type": "success"}
                    response_json_string = json.dumps(response_json)

                    conn.send(response_json_string.encode('utf-8'))

                    broadcast_msg = decoded_data_json["message"]
                    prev_broadcast_list = decoded_data_json["broadcast_sent_to"]

                    print ("Broadcast recieved: " + broadcast_msg)

                    new_sent_list = prev_broadcast_list + self.peer_list

                    node_info = {
                        "address": self.server.server_ip,
                        "port": self.server.server_port
                    }

                    for peer in self.peer_list:
                        if not peer in prev_broadcast_list:
                            broadcast_message_thread = PeerBroadcast(peer, broadcast_msg, new_sent_list, node_info)
                            broadcast_message_thread.start()
                        else:
                            print ("Peer already got message!")


            except Exception as err:
                print ("conn error: " + str(err))
                break


class Server_P2P(threading.Thread):

    def __init__(self, peer_list, server_ip, server_port):
        threading.Thread.__init__(self)
        self.peer_list = peer_list
        self.server_ip = server_ip
        self.server_port = server_port
        self.session_end = False

    def stop(self):
        self.session_end = True

    def run(self):

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.server_ip, self.server_port))
        server_socket.settimeout(2.0)
        server_socket.listen(3)

        print ("Server socket hosted on " + str(self.server_ip) + ":" + str(self.server_port))

        print (str(self.peer_list))

        while not self.session_end:

            try:
                (nodesocket, address) = server_socket.accept()

                conn_thread = PeerHandler(nodesocket, self.peer_list, self)
                conn_thread.start()
            except socket.timeout:
                continue

        server_socket.close()

        print ("Server closed")

    def join(self):
        threading.Thread.join(self)

    def exit(self):
        self.stop()
        self.join()
