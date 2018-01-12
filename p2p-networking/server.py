import socket

import threading

TCP_IP = "127.0.0.1"
TCP_PORT = 5007
BUFFER_SIZE = 20

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((TCP_IP, TCP_PORT))
s.listen(3)

sessions = []
conns = []

def conn_worker(client_socket):

    while True:

        data = client_socket.recv(BUFFER_SIZE)

        if not data:
            break

        for conn in conns:
            broadcast = data

            try:
                conn.send(broadcast)
            except BrokenPipeError:
                conns.remove(conn)


    conns.remove(client_socket)
    client_socket.close()

while 1:

    (clientsocket, address) = s.accept()

    ct = threading.Thread(target=conn_worker, args = (clientsocket,))
    sessions.append(ct)
    conns.append(clientsocket)

    ct.start()

s.close()
