import socket
import sys
import threading
import os

BUFFER = 1024
HOST = "localhost"
PORT = 65535

sock = socket.socket()
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.connect((HOST, PORT))
username = None


def user_input():
    while True:
        msg = sys.stdin.readline()[:-1]

        if username is None:
            ''' username prompt '''
            sock.send(('/username ' + msg).encode())

        else:
            if msg.startswith('/file'):
                _split = msg.split(' ')
                to = _split[1]
                filename = _split[2]
                path = os.path.join(username, filename)
                size = os.path.getsize(path)

                sock.send(('%s %d' % (msg, size)).encode())
                with open(path, 'rb') as f:
                    sock.send(f.read())
                print('File sent (%s:%d) to %s. ' % (filename, size, to))

            else:
                sock.send(msg.encode())


threading.Thread(target=user_input).start()

while True:
    request = sock.recv(BUFFER).decode()

    if request:
        if request.startswith('/username'):
            _split = request.split(' ',)
            username = _split[1]
            if not os.path.exists(username):
                os.makedirs(username)

        elif request.startswith('/file'):
            _split = request.split(' ')
            sender = _split[1]
            filename = _split[2]
            size = int(_split[3])
            path = os.path.join(username, filename)

            with open(path, 'wb') as f:
                while size > 0:
                    piece = sock.recv(min(BUFFER, size))
                    f.write(piece)
                    size -= BUFFER
            print('%s sent a file (%s).' % (sender, filename))

        else:
            print(request)

    else:
        break

sock.close()
if os.path.exists(username):
    os.removedirs(username)