from peerhttp import PeerHTTP


## Test posting of new peer

external_ip = PeerHTTP.get_external_ip()
internal_ip = PeerHTTP.get_local_ip()
test_port = 25565

worked = PeerHTTP.post_local_peer(external_ip, internal_ip, test_port)

print (str(worked))
## Test retrieval of peer list

peer_list = PeerHTTP.get_peer_list()
print ("Peer list: " + str(peer_list))


local_peer_list = PeerHTTP.retrieve_local_peer_list(external_ip)
print ("Local Peer List: " + str(local_peer_list))

# Retrieve random peer

rando_peer = PeerHTTP.retrieve_random_local_peer(external_ip)
print ("Rando Peer: " + str(rando_peer))
