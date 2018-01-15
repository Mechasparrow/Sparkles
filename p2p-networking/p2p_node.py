import socket
import time
import threading
import random

import json
import copy
import sys

BUFFER_SIZE = 1024
session_end = False

## Find peers

## TODO do on LAN

PEER_IP = "127.0.0.1"

start_port = 3000

PEER_LIST = []

for port in range(start_port, start_port + 3000):
    try:
        node_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        node_socket.settimeout(2.0)
        node_socket.connect((PEER_IP, port))

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
                    "address": PEER_IP,
                    "port": port
                }

                PEER_LIST.append(peer_info)

            else:
                continue
        except socket.timeout:
            print ("invalid node")
            continue

        node_socket.close()

    except ConnectionRefusedError:
        continue;

## Server code

def handle_peer_connection(conn):

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

                PEER_LIST.append(actual_peer_info)

                print (PEER_LIST)

                response_json = {"message_type": "success"}
                response_json_string = json.dumps(response_json)

                conn.send(response_json_string.encode('utf-8'))
            elif (decoded_data_json["message_type"] == "peer_list"):

                peer_list_json = {
                    "message_type": "peer_list",
                    "peer_list": PEER_LIST
                }

                peer_list_json_string = json.dumps(peer_list_json)

                conn.send(peer_list_json_string.encode('utf-8'))
        except Exception:
            print ("conn error")
            break

    conn.close()
    print ("PEER DISCONNECT")

SERVER_IP = "127.0.0.1"
SERVER_PORT = random.randint(start_port, start_port + 3000)

def server_routine():

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.settimeout(2.0)
    server_socket.listen(3)

    print ("Server socket hosted on " + SERVER_IP + ":" + str(SERVER_PORT))

    print (str(PEER_LIST))

    global session_end

    while not session_end:

        try:
            (nodesocket, address) = server_socket.accept()

            conn_thread = threading.Thread(target = handle_peer_connection, args = (nodesocket, ))
            conn_thread.start()
        except socket.timeout:
            continue

    server_socket.close()

    print ("Server closed")

## Client code

def message_gen(message):

    json_message = {
        "message_type": "message",
        "content": message
    }

    json_message_string = json.dumps(json_message)

def merge_peer_list(old_peer_list, new_peer_list):

    ## Remove self from list

    self_info = {
        "address": SERVER_IP,
        "port": SERVER_PORT
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

def peer_list_retrieval(peer):

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

            peer_conn.send(peer_info_string.encode('utf-8'))

            response_data = peer_conn.recv(BUFFER_SIZE).decode('utf-8')
            response_data_json = json.loads(response_data)

            if (response_data_json["message_type"] == "peer_list"):

                new_peer_list = response_data_json["peer_list"]

                global PEER_LIST
                NEW_PEER_LIST = merge_peer_list(PEER_LIST, new_peer_list)

                print ()
                print ("NEW LIST: " + str(NEW_PEER_LIST))


                PEER_LIST = NEW_PEER_LIST

            else:
                print ("PEER FAILURE")

            peer_conn.close()
            return

        except socket.timeout:
            print ("unable to send peer info")
            return
    except ConnectionRefusedError:
        print ("connection refused")

    pass

def send_peer_server_info(peer):

    PEER_IP = peer["address"]
    PORT = peer["port"]

    peer_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    peer_conn.settimeout(2.0)
    peer_conn.connect((peer["address"], peer["port"]))

    peer_info_json = {
        "message_type": "peer_info",
        "content": {
            "ip": SERVER_IP,
            "port": SERVER_PORT
        }
    }

    peer_info_string = json.dumps(peer_info_json)

    try:

        try:

            peer_conn.send(peer_info_string.encode('utf-8'))

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


## FIXME
def broadcast_message():

    pass

def client_routine():
    print ("client code")

    global PEER_LIST

    # TODO Send server information to fellow est peers

    for peer in PEER_LIST:
        print (peer)
        peer_info_thread = threading.Thread(target=send_peer_server_info, args = (peer,))
        peer_info_thread.start()

    # TODO sync peer list

    list_threads = []

    for peer in PEER_LIST:
        peer_list_thread = threading.Thread(target=peer_list_retrieval, args = (peer,))
        peer_list_thread.start()
        list_threads.append(peer_list_thread)

    for list_thread in list_threads:
        list_thread.join()

    print ()
    print ("FINAL: " + str(PEER_LIST))

    # TODO broadcast *messages* over the network

    while True:

        message = input ("what would you like to broadcast? (exit): ")

        if (message == "exit"):
            print ("exiting")
        else:

            for peer in PEER_LIST:

                ## TODO implement broadcast_message()

                broadcast_message_thread = threading.Thread(target=broadcast_message, args = (message,))
                broadcast_message_thread.start()


    return

server_thread = threading.Thread(target=server_routine)
client_thread = threading.Thread(target=client_routine)

server_thread.start()
client_thread.start()

client_thread.join()
session_end = True
