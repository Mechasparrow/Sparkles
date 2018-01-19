import socket
import http.client
import json

import requests

import urllib.request
import random

## REFACTOR

class PeerHTTP:

    def get_peer_list():

        response = requests.get('https://sparkles-list.glitch.me/peers')

        return response.json()

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

        response = requests.post("https://sparkles-list.glitch.me/connect", data = payload)

        status_code = response.status_code

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

        payload_json = json.dumps(payload)

        headers = {
            "Content-type": "application/json",
            "Accept": "text/plain"
        }

        response = requests.post("https://sparkles-list.glitch.me/connect", data = payload)

        status_code = response.status_code

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
        external_ip = requests.get('http://ident.me').text
        return external_ip
