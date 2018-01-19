import socket
import time
import threading
import random

import json
import copy
import sys

from peerhttp import PeerHTTP

# Import p2p server
from server_p2p_node import Server_P2P

# Import p2p client
from client_p2p_node import Client_P2P

# Import broadcast protocol
from peer_broadcast import PeerBroadcast

BUFFER_SIZE = 1024

## Find peers
EXTERNAL_IP = PeerHTTP.get_external_ip()

## TODO do on LAN

PEER_IP = PeerHTTP.get_local_ip()

start_port = 3000

PEER_LIST = []

LOCAL_PEER_LIST = PeerHTTP.retrieve_local_peer_list(EXTERNAL_IP)

for peer in LOCAL_PEER_LIST:

    peer_hash = peer["hash"]

    try:
        node_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        node_socket.settimeout(2.0)

        peer_ip = peer['external']
        peer_port = int(peer['port'])

        if (peer['type'] == "local"):
            peer_ip = peer['internal']
        else:
            peer_ip = peer['external']

        node_socket.connect((peer_ip, peer_port))

        try:

            test_peer_message = {
                "message_type": "est_conn"
            }

            test_peer_string = json.dumps(test_peer_message)

            node_socket.send(test_peer_string.encode('utf-8'))

            verify_message = node_socket.recv(BUFFER_SIZE).decode('utf-8')

            if (verify_message == "SPARKLENODE"):
                print ("valid node found!")

                peer_info = {
                    "address": peer_ip,
                    "port": peer_port
                }

                PEER_LIST.append(peer_info)

            else:
                continue
        except socket.timeout:
            print ("invalid node")
            PeerHTTP.delete_peer(peer_hash)
            continue

        node_socket.close()

    except ConnectionRefusedError:
        PeerHTTP.delete_peer(peer_hash)
        continue
    except socket.timeout:
        print ("dead node")
        PeerHTTP.delete_peer(peer_hash)
        continue
    except Exception as err:
        print ("weird node")
        PeerHTTP.delete_peer(peer_hash)
        continue

## Server code

SERVER_IP = PeerHTTP.get_local_ip()
SERVER_PORT = random.randint(start_port, start_port + 3000)

post_peer = PeerHTTP.post_local_peer(EXTERNAL_IP, SERVER_IP, SERVER_PORT)

if (post_peer):
    print ("Server posted")
else:
    print ("Server not posted")

server_thread = Server_P2P(PEER_LIST, SERVER_IP, SERVER_PORT)
client_thread = Client_P2P(PEER_LIST, server_thread)

server_thread.start()
client_thread.start()

client_thread.join()
server_thread.exit()
