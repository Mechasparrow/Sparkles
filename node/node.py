from socketIO_client import SocketIO, LoggingNamespace

def on_connect():
    print ('connected to backend')

def on_message_response(*args):
    message = args[0]['data']
    print (message)

socketIO = SocketIO('localhost', 8000, LoggingNamespace)

socketIO.send('hello there')
socketIO.emit("message");
socketIO.on('message_response', on_message_response)
socketIO.wait(seconds=1)
