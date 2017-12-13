import socket
import sys
import threading
import os

#inisialisasi
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#proses binding
server_address = ('localhost', 9001)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

#listening
sock.listen(1)

def response_list():
	filegambar = os.listdir(".")
	panjang = 255
	hasil = "HTTP/1.1 200 OK\r\n" \
		"Content-Type: text/plain\r\n" \
		"Content-Length: {}\r\n" \
		"\r\n" \
		"{}" . format(panjang, filegambar)
	return hasil

def response_download(url):
    method, namafile = url.split(':')
    apakek = open (namafile,'r').read()
    panjang = len(apakek)
    hasil = "HTTP/1.1 200 OK\r\n" \
		"Content-Type: multipart/form-data\r\n" \
		"Content-Length: {}\r\n" \
		"\r\n" \
		"{}" . format(panjang, apakek)
    return hasil

def response_hapus(url):
	method, namafile = url.split(':')
	apakek = os.system('rm ' + namafile)
	hasil = "HTTP/1.1 200 OK\r\n" \
		"Content-Type: text/plain\r\n" \
		"Content-Length: 6\r\n" \
		"\r\n" \
		"SUKSES"
	return hasil
	
def response_tambahdirect(url):
	method, namafile = url.split(':')
	apakek = os.system('mkdir ' + namafile)
	hasil = "HTTP/1.1 200 OK\r\n" \
		"Content-Type: text/plain\r\n" \
		"Content-Length: 6\r\n" \
		"\r\n" \
		"SUKSES"
	return hasil
	
	#durung isok
def response_hapusdirect(url):
	method, namafile = url.split(':')
	apakek = os.rmdir(namafile)
	hasil = "HTTP/1.1 200 OK\r\n" \
		"Content-Type: text/plain\r\n" \
		"Content-Length: 6\r\n" \
		"\r\n" \
		"SUKSES"
	return hasil
	
def response_pindahdirect(url):
	method, namafile, tujuan = url.split(':')
	apakek = os.system('mv ' + namafile + ' ' + tujuan)
	hasil = "HTTP/1.1 200 OK\r\n" \
		"Content-Type: text/plain\r\n" \
		"Content-Length: 6\r\n" \
		"\r\n" \
		"SUKSES"
	return hasil

def response_pindahfile(url):
	method, namafile, tujuan = url.split(':')
	apakek = os.system('mv ' + namafile + ' ' + tujuan)
	hasil = "HTTP/1.1 200 OK\r\n" \
		"Content-Type: text/plain\r\n" \
		"Content-Length: 6\r\n" \
		"\r\n" \
		"SUKSES"
	return hasil

def response_redirect():
	hasil = "HTTP/1.1 301 Moved Permanently\r\n" \
		"Location: {}\r\n" \
		"\r\n"  . format('http://www.its.ac.id')
	return hasil




#fungsi melayani client
def layani_client(koneksi_client,alamat_client):
    try:
       print >>sys.stderr, 'ada koneksi dari ', alamat_client
       request_message = ''
       while True:
           data = koneksi_client.recv(64)
	   data = bytes.decode(data)
           request_message = request_message+data
	   if (request_message[-4:]=="\r\n\r\n"):
		break

       baris = request_message.split("\r\n")
       baris_request = baris[0]
       print baris_request
 	
       a,url,c = baris_request.split(" ")
       
       if ('/download' in url):
          respon = response_download(url)
       elif ('/delete' in url):
          respon = response_hapus(url)
       elif ('/adddirect' in url):
          respon = response_tambahdirect(url)
       elif ('/deletedirect' in url):
          respon = response_hapusdirect(url)
       elif ('/movedirect' in url):
          respon = response_pindahdirect(url)
       elif ('/movefile' in url):
          respon = response_pindahfile(url)
       else:
          respon = response_list()

       koneksi_client.send(respon)
    finally:
        # Clean up the connection
        koneksi_client.close()


while True:
    # Wait for a connection
    print >>sys.stderr, 'waiting for a connection'
    koneksi_client, alamat_client = sock.accept()
    s = threading.Thread(target=layani_client, args=(koneksi_client,alamat_client))
    s.start()

