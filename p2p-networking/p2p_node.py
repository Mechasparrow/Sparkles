import socket
import time
import threading
import random


BUFFER_SIZE = 1024
session_end = False

## Find peers

PEER_IP = "127.0.0.1"

start_port = 3000

PEER_LIST = []

for port in range(start_port, start_port + 3000):
    try:
        node_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        node_socket.settimeout(2.0)
        node_socket.connect((PEER_IP, port))

        try:
            verify_message = node_socket.recv(BUFFER_SIZE).decode('utf-8')

            if (verify_message == "SPARKLENODE"):
                print ("valid node found!")

                peer_info = {
                    "address": PEER_IP,
                    "port": port
                }

                PEER_LIST.append(peer_info)

                break
            else:
                continue
        except socket.timeout:
            print ("invalid node")
            continue

    except ConnectionRefusedError:
        continue;

## Server code

def server_routine():
    SERVER_IP = "127.0.0.1"
    SERVER_PORT = random.randint(start_port, start_port + 3000)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.listen(3)

    print ("Server socket hosted on " + SERVER_IP + ":" + str(SERVER_PORT))

    print (str(PEER_LIST))

    while 1:

        (nodesocket, address) = server_socket.accept()

        nodesocket.send("SPARKLENODE".encode('utf-8'))

        # TODO Handle request for peer list

        node_info = nodesocket.recv(BUFFER_SIZE)

        print (node_info.decode('utf-8'))

    server_socket.close()

    print ("Server closed")

## Client code

def client_routine():
    print ("client code")

    # TODO Send server information to fellow est peers

    # TODO sync peer list

    # TODO broadcast *messages* over the network

    pass

server_thread = threading.Thread(target=server_routine)
client_thread = threading.Thread(target=client_routine)

server_thread.start()
client_thread.start()
