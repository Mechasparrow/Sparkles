import socket
from peerhttp import PeerHTTP

import json

BUFFER_SIZE = 1024

def local_search(external_ip):
    peer_list = []

    LOCAL_PEER_LIST = PeerHTTP.retrieve_local_peer_list(external_ip)

    for peer in LOCAL_PEER_LIST:

        peer_hash = peer["hash"]

        try:
            node_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            node_socket.settimeout(2.0)

            peer_ip = peer['internal']
            peer_port = int(peer['port'])

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

                    peer_list.append(peer_info)

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
            print (err)
            PeerHTTP.delete_peer(peer_hash)
            continue

    return peer_list
