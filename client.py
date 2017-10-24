import websocket
from websocket import create_connection

ws = create_connection("ws://sparkle-coin-server.herokuapp.com")

ws.send("hello there")

result = ws.recv()

print (result)
