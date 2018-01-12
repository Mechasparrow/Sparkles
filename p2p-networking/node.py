import socket
import time
import threading


TCP_IP = "127.0.0.1"
TCP_PORT = 5007
BUFFER_SIZE = 1024

session_end = False

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(3.0)
s.connect((TCP_IP, TCP_PORT))

def handler(user_socket):

    while True:

        if (session_end == True):
            break

        try:
            data = user_socket.recv(BUFFER_SIZE)

            if (data == None):
                break

            print()
            print ("Broadcast: " + data.decode('utf-8'))
        except socket.timeout:
            continue

user_handler = threading.Thread(target=handler, args = (s,))
user_handler.start()

while not session_end:

    time.sleep(0.1)

    input_data = input("What would you like to send? (exit): ")
    print ()

    if (input_data == "exit"):
        session_end = True
        print ("session end")
        user_handler.join()
        break

    s.send(input_data.encode('utf-8'))

s.close()
