import threading

from peer_broadcast import PeerBroadcast








class Client_P2P(threading.Threading):

    def __init__(self, peer_list, server):
        threading.Threading.__init__(self)
        self.peer_list = peer_list
        self.server_ip = server.server_ip
        self.server_port = server.server_port

    def run(self):
        print ("client code")

        # Send server information to fellow est peers

        for peer in self.peer_list:
            print (peer)
            peer_info_thread = threading.Thread(target=send_peer_server_info, args = (peer,))
            peer_info_thread.start()

        # sync peer list

        list_threads = []

        for peer in self.peer_list:
            peer_list_thread = threading.Thread(target=peer_list_retrieval, args = (peer,))
            peer_list_thread.start()
            list_threads.append(peer_list_thread)

        for list_thread in list_threads:
            list_thread.join()

        print ()
        print ("FINAL: " + str(self.peer_list))

        while True:

            # Broadcast messages

            message = input ("what would you like to broadcast? (exit): ")

            if (message == "exit"):
                print ("exiting")
                break
            else:

                node_info = {
                    "address": self.server_ip,
                    "port": self.server_port
                }

                for peer in self.peer_list:
                    broadcast_message_thread = PeerBroadcast(peer, message,PEER_LIST, node_info)
                    broadcast_message_thread.start()
