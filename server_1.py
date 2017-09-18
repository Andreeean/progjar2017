import sys
import socket
from lib import *

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 17000)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

sock.listen(1)

while True:
	print >>sys.stderr, 'Waiting for connection'
	socket_si_client, client_address = sock.accept()
	print >>sys.stderr, 'connection from', client_address
	pesan_dari_client = socket_si_client.recv(100)
	cmd, param1, param2 = pesan_dari_client.split(" ")
	hasil = fungsi(cmd,param1,param2)
	socket_si_client.sendall(str(hasil)+"\n")
	socket_si_client.close()
