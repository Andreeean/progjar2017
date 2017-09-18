import sys
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('10.151.252.142', 13000)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

sock.listen(1)

while True:
	print >>sys.stderr, 'waiting for a connection'
	socket_si_client, client_address = sock.accept()
	print >>sys.stderr, 'connection from', client_address
	pesan_dari_client = socket_si_client.recv(100)
	#socket_si_client.sendall("dari server -> "+pesan_dari_client)
	print pesan_dari_client
	socket_si_client.close()
