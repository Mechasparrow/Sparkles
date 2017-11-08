import websocket
from websocket import create_connection
import time

ws = create_connection("ws://localhost:5000/miners")
ws.send("yo")
ws.close()
