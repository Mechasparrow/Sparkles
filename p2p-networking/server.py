import socket

TCP_IP = "127.0.0.1"
TCP_PORT = 5007
BUFFER_SIZE = 20

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

die = False

while die == False:

    conn, addr = s.accept()

    print ('Connection address:' + str(addr))
    while True:
        data = conn.recv(BUFFER_SIZE)
        data_decoded = data.decode("utf-8")

        if (data_decoded == "exit"):
            die = True
            dead_msg = "Connection dead".encode("utf-8")
            conn.send(dead_msg)
            break

        if not data:
            break

        print ("recieved data:" + data_decoded)
        conn.send(data) #echo

    conn.close()

s.close()
