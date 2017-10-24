import websocket
from websocket import create_connection

ws = create_connection("ws://localhost:5000/echo")

ws.send("hello there")

result = ws.recv()

print (result)
