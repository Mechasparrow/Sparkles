import websocket
import _thread
import time
import json

def on_message(ws, message):
    print (message)

def on_error(ws, error):
    print (error)

def on_close(ws):
    print ("### closed ###")

def on_open(ws):
    print ("### open ###")
    ws.send("wallet connect")

    def run (*args):
        while (True):
            mode = input("What would you like to do? (transaction, balance, exit, nodes): ")

            if (mode == "exit"):
                ws.send("wallet disconnect")
                ws.close()
                break
            elif (mode == "transaction"):
                print ("beginning transaction...")
                amnt = input("How much would you like to send?: ")
                address = input("What is the address of the recipient?: ")

                transaction_data = {
                    "message_type": "transaction",
                    "data": {
                        "amnt": amnt,
                        "address": address
                    }
                }

                transaction_json = json.dumps(transaction_data)
                ws.send(transaction_json)



            elif (mode == "nodes"):
                ws.send("get nodes")
                time.sleep(1)
        print ("thread terminating")

    _thread.start_new_thread(run, ())

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://localhost:5000/wallet",
        on_message = on_message,
        on_error = on_error,
        on_close = on_close
    )

    ws.on_open = on_open
    ws.run_forever()
