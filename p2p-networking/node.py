import socket
import time

TCP_IP = "127.0.0.1"
TCP_PORT = 5007
BUFFER_SIZE = 1024

session_end = False

while not session_end:

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))

    session_msg = input("Message to send (exit to exit): ")

    s.send(session_msg.encode("utf-8"))
    data = s.recv(BUFFER_SIZE)
    print ("received data: " + data.decode('utf-8'))

    if (data.decode("utf-8") == "Connection dead"):
        session_end = True
        break

    s.close()
    time.sleep(0.1)
