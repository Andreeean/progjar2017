import sys
import socket
from lib import *
from threading import Thread

def proses_baris(baris):
	try:
		cmd,param1,param2 = baris.split(" ")
		hasil = fungsi(cmd,param1,param2)
	except ValueError:
		hasil = 'ERR'
	return hasil

def handle_client(socket_si_client,client_address):
	print "koneksi dari %s \r\n" % (str(client_address))
	pesan_dari_client=''
	while True:
		data = socket_si_client.recv(20)
		if not data:
			print "socket diclose paksa\r\n"
			break
		pesan_dari_client = pesan_dari_client+data
		if pesan_dari_client.startswith("QUIT"):
			socket_si_client.sendall("Bye\r\n")
			socket_si_client.close()
			break
		elif pesan_dari_client.endswith("\r\n"):
			hasil = proses_baris(pesan_dari_client)
			socket_si_client.sendall(str(hasil)+"\r\n")
			pesan_dari_client = ''

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 14001)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

sock.listen(1)

while True:
	print >>sys.stderr, 'Waiting for connection'
	socket_si_client, client_address = sock.accept()
	print >>sys.stderr, 'connection from', client_address
	client_process = Thread(target=handle_client,args=(socket_si_client,client_address,))
	client_process.start()
