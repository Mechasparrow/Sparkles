import socket

def recvall(conn):

    text = ''

    try:
        chunk = ''

        while True:
            chunk += conn.recv()
            if not chunk:
                break
        else:
            text += chunk

    except Exception:
        if text:
            pass
        else:
            return False

    return text
