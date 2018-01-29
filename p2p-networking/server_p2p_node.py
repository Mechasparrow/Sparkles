import threading

import socket
import json

from peer_broadcast import PeerBroadcast

from socket_recieve_all import recvall

BUFFER_SIZE = 1024

# The handler for peer connections
class PeerHandler(threading.Thread):

    def __init__(self, conn, peer_list, server, handlers):
        threading.Thread.__init__(self)
        self.conn = conn
        self.peer_list = peer_list
        self.server = server
        self.handlers = handlers

    def broadcast_msg(self, msg, broadcast_list = None, sent_list = None):

        if (sent_list == None):
            sent_list = self.peer_list

        if (broadcast_list == None):
            broadcast_list = []

        node_info = {
            "address": self.server.server_ip,
            "port": self.server.server_port
        }

        broadcast_list.append(node_info)

        for peer in self.peer_list:
            if not peer in broadcast_list:
                broadcast_message_thread = PeerBroadcast(peer, msg, sent_list, node_info)
                broadcast_message_thread.start()
            else:
                print ("Peer already got message!")

    def propagate_msg(self, broadcast_data):
        broadcast_message = broadcast_data["message"]
        prev_broadcast_list = broadcast_data["broadcast_sent_to"]

        print ("Broadcast recieved: " + broadcast_message)

        new_sent_list = prev_broadcast_list + self.peer_list

        self.broadcast_msg(broadcast_message, broadcast_list = prev_broadcast_list, sent_list = new_sent_list)

    def run(self):

        print ("handling connection...")

        conn = self.conn

        while True:

            try:
                data = recvall(conn)
                print (data)


                if not data:
                    break

                decoded_data = data.decode("utf-8")
                decoded_data_json = json.loads(decoded_data)

                print (decoded_data_json)

                if (decoded_data_json["message_type"] == "est_conn"):
                    verify_response = "SPARKLENODE"
                    print ("peer connected!")
                    conn.sendall(verify_response.encode('utf-8'))
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

                    conn.sendall(response_json_string.encode('utf-8'))
                elif (decoded_data_json["message_type"] == "peer_list"):

                    peer_list_json = {
                        "message_type": "peer_list",
                        "peer_list": self.peer_list
                    }

                    peer_list_json_string = json.dumps(peer_list_json)

                    conn.sendall(peer_list_json_string.encode('utf-8'))
                elif (decoded_data_json["message_type"] == "broadcast"):

                    response_json = {"message_type": "success"}
                    response_json_string = json.dumps(response_json)

                    conn.sendall(response_json_string.encode('utf-8'))

                    self.propagate_msg(decoded_data_json)

                    try:
                        raw_payload = decoded_data_json["message"]
                        payload = json.loads(raw_payload)
                        payload_header = payload["message_type"]

                        if payload_header in self.handlers:
                            self.handlers[payload_header](self.broadcast_msg, payload)
                        else:
                            print ("Not a valid command")

                    except Exception as err:
                        print ("NOT PAYLOAD")


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
        self.handlers = {}

    def add_handler(self, handler_name, handler):
        self.handlers[handler_name] = handler

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

                conn_thread = PeerHandler(conn = nodesocket, peer_list = self.peer_list, server=self, handlers=self.handlers)
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
