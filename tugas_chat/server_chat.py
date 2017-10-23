# chat_server.py
 
import sys
import socket
import select

HOST = 'localhost' 
SOCKET_LIST = []
RECV_BUFFER = 4096 
PORT = 9000
username = {}

def chat_server():

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(10)
 
    # add server socket object to the list of readable connections
    SOCKET_LIST.append(server_socket)
 
    print "Chat server started on port " + str(PORT)
    print "Hostname " + str(HOST)
 
    while 1:
        
        # get the list sockets which are ready to be read through select
        # 4th arg, time_out  = 0 : poll and never block
        ready_to_read,ready_to_write,in_error = select.select(SOCKET_LIST,[],[],0)
      
        for sock in ready_to_read:
            # a new connection request recieved
            #print "ready to read"
            if sock == server_socket: 
                sockfd, addr = server_socket.accept()
                SOCKET_LIST.append(sockfd)
             
            # a message from a client, not a new connection
            else:
                #print hasattr (sock, 'name')
                if not username.get (sock):
                    data = sock.recv(RECV_BUFFER)
                    print [s for s in username.iteritems()]
                    if data in [username[key] for key in username.iterkeys ()]:
                        sock.send("Username is already taken!\n")
                        continue
                    username[sock] = data
                    print "Client (%s) connected" % username[sock]
                    broadcast(server_socket, sockfd, "[%s] entered our chatting room\n" % username[sock])
                    continue
                # process data recieved from client, 
                try:
                    # receiving data from the socket.
                    data = sock.recv(RECV_BUFFER)
                    
                    if data:
                        if data.startswith('FILE'):
                            print ('FILE')
                            data = sock.recv(4096)
                            print data
                            target = sock.recv(4096)
                            print target
                            for s in SOCKET_LIST:
                                if username[s] == target:
                                    sock2 = s
                                    break
                            print sock2
                            sock2.send ('FILE')
                            with open('received_file', 'wb') as f:
                                #print 'file opened'
                                while True:
                                    print('receiving data...')
                                    data = sock.recv(4096)
                                    if not data:
                                        break
                                    # write data to a file
                                    f.write(data)
                                    
                            f = open('received_file','rb')
                            l = f.read(4096)
                            while (l):
                                sock2.send(l)
                                l = f.read(4096)
                            f.close()
                                    
                        else :    
                            # there is something in the socket
                            broadcast(server_socket, sock, "\r" + '=>[' + username[sock] + '] ' + data + '\n')
                    else:
                        # remove the socket that's broken 
                        
                        if sock in SOCKET_LIST:
                            SOCKET_LIST.remove(sock)

                        # at this stage, no data means probably the connection has been broken
                        broadcast(server_socket, sock, "Client (%s) is offline\n" % username[sock])
                        username.pop(sock, None)

                # exception 
                except:
                    broadcast(server_socket, sock, "Client (%s) is offline\n" % username[sock])
                    continue

    server_socket.close()
    
# broadcast chat messages to all connected clients
def broadcast (server_socket, sock, message):
    for socket in SOCKET_LIST:
        # send the message only to peer
        if socket != server_socket and socket != sock :
            try :
                socket.send(message)
            except :
                # broken socket connection
                socket.close()
                # broken socket, remove it
                if socket in SOCKET_LIST:
                    SOCKET_LIST.remove(socket)
 
if __name__ == "__main__":

    sys.exit(chat_server())
