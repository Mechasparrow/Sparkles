import socket
import http.client

import urllib.request

class PeerHTTP:

    def get_peer_list():

        pass

    def post_local_peer():

        pass


    def get_local_ip():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip

    def get_external_ip():

        external_ip = urllib.request.urlopen('http://ident.me').read().decode('utf-8')
        return external_ip
