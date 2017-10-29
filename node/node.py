from socketIO_client import SocketIO, LoggingNamespace

def on_connect():
    print ('connected to backend')

def on_message(message):
    print (message)

socketIO = SocketIO('localhost', 8000, LoggingNamespace)

socketIO.send('connect')
socketIO.wait(seconds=1)

socketIO.on('message', on_message)
