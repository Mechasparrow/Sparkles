import socket
import http.client
import json

import urllib.request
import random

class PeerHTTP:

    def get_peer_list():

        conn = http.client.HTTPSConnection("sparkles-list.glitch.me")

        conn.request("GET", url = "/peers")
        response = conn.getresponse()

        raw_response = response.read()
        json_response_string = raw_response.decode('utf-8')

        return json.loads(json_response_string)

    def retrieve_local_peer_list(external_ip):

        # TODO retrieve local peer list

        peer_list = PeerHTTP.get_peer_list()

        local_peer_list = [item for item in peer_list if item['type'] == "local" and item['external'] == external_ip]

        return local_peer_list

    def retrieve_random_local_peer(external_ip):

        # TODO retrieve a random local peer

        local_peer_list = PeerHTTP.retrieve_local_peer_list(external_ip)

        peer_node = random.choice(local_peer_list)

        return peer_node

    def post_external_peer(external_ip, port):

        payload = {
            "external": external_ip,
            "internal": "0.0.0.0",
            "port": port,
            "type": "public"
        }

        conn = http.client.HTTPSConnection("sparkles-list.glitch.me")
        payload_json = json.dumps(payload)

        headers = {
            "Content-type": "application/json",
            "Accept": "text/plain"
        }

        conn.request("POST", url = "/connect", body = payload_json, headers = headers )
        response = conn.getresponse()
        response_raw_data = response.read()

        response_json_string = response_raw_data.decode('utf-8')

        status_code = response.status

        if (status_code == 200):
            return True
        else:
            return False


    def post_local_peer(external_ip, local_ip, port):

        payload = {
            "external": external_ip,
            "internal": local_ip,
            "port": port,
            "type": "local"
        }

        conn = http.client.HTTPSConnection("sparkles-list.glitch.me")
        payload_json = json.dumps(payload)

        headers = {
            "Content-type": "application/json",
            "Accept": "text/plain"
        }

        conn.request("POST", url = "/connect", body = payload_json, headers = headers )
        response = conn.getresponse()
        response_raw_data = response.read()

        response_json_string = response_raw_data.decode('utf-8')

        status_code = response.status

        if (status_code == 200):
            return True
        else:
            return False


    def get_local_ip():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip

    def get_external_ip():

        external_ip = urllib.request.urlopen('http://ident.me').read().decode('utf-8')
        return external_ip
