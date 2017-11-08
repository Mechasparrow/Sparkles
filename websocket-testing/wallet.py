import websocket
import _thread
import time

def on_message(ws, message):
    if (message == "terminate"):
        ws.close()

def on_error(ws, error):
    print (error)

def on_close(ws):
    print ("### closed ###")

def on_open(ws):
    print ("### open ###")

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://localhost:5000/wallet",
        on_message = on_message,
        on_error = on_error,
        on_close = on_close
    )

    ws.on_open = on_open
    ws.run_forever()
