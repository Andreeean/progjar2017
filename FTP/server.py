import socket
import threading
import os

def retrfile(name, sock) :
	filename = sock.recv(1024)
	if os.path.isfile(filename):
		print "test"
		sock.send("EXIST " + str(os.path.getsize(filename)))
		userresponse = sock.recv(1024)
		if userresponse[:2] == 'OK':
			with open(filename, 'rb') as f:
				bytestosend = f.read(1024)
				sock.send(bytestosend)
				while bytestosend != "":
					bytestosend = f.read(1024)
					sock.send(bytestosend)

	else:
		sock.send("ERROR")

	sock.close()

def main():
	host = 'localhost'
	port = 5000

	s = socket.socket()
	s.bind((host, port))

	s.listen(5)

	print "Server started"
	while True:
		c, addr = s.accept()
		print "Client connected ip: <" + str(addr) + ">"
		t = threading.Thread(target=retrfile, args=("retrThread", c))
		t.start()

	s.close()

if __name__ == '__main__':
	main()
