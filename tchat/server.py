import socket as pysocket
import select
import re
import os

BUFFER = 1024
HOST = "localhost"
PORT = 65535
SERVER_MEDIA_PATH = 'server/media'

server_socket = pysocket.socket()
server_socket.setsockopt(pysocket.SOL_SOCKET, pysocket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen()
sockets = [server_socket]
ftp_sockets = []
clients = {}
usernames = {}

if not os.path.exists(SERVER_MEDIA_PATH):
    os.makedirs(SERVER_MEDIA_PATH)

print('Server ready. Port: %d' % PORT)

while True:
    read_ready, write_ready, exception = select.select(sockets, [], [])

    for sock in read_ready:
        if sock is server_socket:
            socket, address = sock.accept()
            sockets.append(socket)
            socket.send(b'Enter Your Username!')
        else:
            request = sock.recv(BUFFER).decode()
            print(request)

            if request:
                if request.startswith('@'):
                    _split = re.split('[@ ]', request,2)
                    username = _split[1]

                    if username in clients.keys():
                        receiver = clients[username]
                        sender = usernames[sock]
                        message = _split[2]
                        receiver.send(('%s: %s' % (sender, message)).encode())
                    else:
                        sock.send(b'Username Not Found!')

                elif request.startswith('/username'):
                    username = request.split(' ',)[1]

                    if username not in clients.keys():
                        clients[username] = sock
                        usernames[sock] = username
                        sock.send(('/username ' + username).encode())
                    else:
                        sock.send(b'Username Already Used!')

                elif request.startswith('/file'):
                    _split = request.split(' ')
                    receiver = clients[_split[1]]
                    filename = _split[2]
                    size = int(_split[3])
                    sender = usernames[sock]
                    path = os.path.join(SERVER_MEDIA_PATH, filename)

                    receiver.send(('/file %s %s %d' % (sender, filename, size)).encode())
                    with open(path, 'wb') as f:
                        while size > 0:
                            piece = sock.recv(min(BUFFER, size))
                            receiver.send(piece)
                            size -= BUFFER
                    print('%s sent a file (%s:%d) to %s.' % (sender, filename, size, usernames[receiver]))

                else:
                    for username, socket in clients.items():
                        socket.send(('%s: %s' % (usernames[sock], request)).encode())

            else:
                ''' a user disconnected '''
                print('%s disconnected.' % usernames[sock])
                sock.close()
                clients.pop(usernames[sock])
                usernames.pop(sock)
                sockets.remove(sock)
