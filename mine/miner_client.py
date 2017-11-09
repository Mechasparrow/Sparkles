import websocket
import _thread
import time
import json

def on_message(ws, message):
    print (message)

def on_error(ws, error):
    print (error)

def on_close(ws):

    close_message = {
        'message_type': 'connection',
        'connection': False
    }

    close_message_json = json.dumps(close_message)
    ws.send(close_message_json)

    print ("### closed ###")

def on_open(ws):
    print ("### open ###")

    open_message = {
        'message_type': 'connection',
        'connection': True
    }

    open_message_json = json.dumps(open_message)

    ws.send(open_message_json)


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://localhost:5000/miners",
        on_message = on_message,
        on_error = on_error,
        on_close = on_close
    )

    ws.on_open = on_open
    ws.run_forever()
