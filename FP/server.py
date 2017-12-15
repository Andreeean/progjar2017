#tian ganteng
#ADIB LEBIH
import socket
import sys
import threading
import os

#INISIALISASI
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#PROSES BINDING
server_address = ('localhost', 9005)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

#LISTENING
sock.listen(1)

#LISTING
def response_list():
	listfile = os.listdir(".")
	panjang = 755
	hasil = "HTTP/1.1 200 OK\r\n" \
		"Content-Type: text/plain\r\n" \
		"Content-Length: {}\r\n" \
		"\r\n" \
		"\nLIST DIRECTORY --> /\nDOWNLOAD --> /download:(namafile)\nUPLOAD --> /upload:(namafile)\nDELETE FILE --> /delete:(namafile)\nDELETE DIRECTORY --> /deletedirect:(namadirectory)\nMOVE FILE --> /movefile:(namafile):(tujuan)\nMOVE DIRECTORY --> /movedirect:(namadirectory):(tujuan)\nADD DIRECTORY --> /adddirect:(namadirectory)\n\n\n<-DIRECTORY->\n\n" \
		"{}". format(panjang, listfile)
	return hasil

#DOWNLOAD
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
    
#UPLOAD
def response_upload(url):
    method, namafile = url.split(':')
    apakek = open (namafile,'r').read()
    panjang = len(apakek)
    hasil = "HTTP/1.1 200 OK\r\n" \
		"Content-Type: multipart/form-data\r\n" \
		"Content-Length: {}\r\n" \
		"\r\n" \
		"{}" . format(panjang, apakek)
    return hasil

#HAPUS FILE GANNN
def response_hapus(url):
	method, namafile = url.split(':')
	apakek = os.system('rm ' + namafile)
	hasil = "HTTP/1.1 200 OK\r\n" \
		"Content-Type: text/plain\r\n" \
		"Content-Length: 25\r\n" \
		"\r\n" \
		"REMOVE FILE SUCCESS!"
	return hasil
	
#BIKIN FOLDER BARU
def response_tambahdirect(url):
	method, namafile = url.split(':')
	apakek = os.system('mkdir ' + namafile)
	hasil = "HTTP/1.1 200 OK\r\n" \
		"Content-Type: text/plain\r\n" \
		"Content-Length: 25\r\n" \
		"\r\n" \
		"ADD DIRECTORY SUCCESS!"
	return hasil
	
#BUAT HAPUS FOLDER	#SAYANG BERIBU SAYANG BELUM BERHASIL
def response_hapusdirect(url):
	method, namafile = url.split(':')
	apakek = os.rmdir(namafile)
	hasil = "HTTP/1.1 200 OK\r\n" \
		"Content-Type: text/plain\r\n" \
		"Content-Length: 26\r\n" \
		"\r\n" \
		"REMOVE DIRECTORY SUCCESS!"
	return hasil
	
#BUAT MINDAHIN FOLDER
def response_pindahdirect(url):
	method, namafile, tujuan = url.split(':')
	apakek = os.system('mv ' + namafile + ' ' + tujuan)
	hasil = "HTTP/1.1 200 OK\r\n" \
		"Content-Type: text/plain\r\n" \
		"Content-Length: 25\r\n" \
		"\r\n" \
		"MOVE DIRECTORY SUCCES!"
	return hasil

#BUAT MINDAHIN FILE
def response_pindahfile(url):
	method, namafile, tujuan = url.split(':')
	apakek = os.system('mv ' + namafile + ' ' + tujuan)
	hasil = "HTTP/1.1 200 OK\r\n" \
		"Content-Type: text/plain\r\n" \
		"Content-Length: 20\r\n" \
		"\r\n" \
		"MOVE FILE SUCCESS!"
	return hasil

# ------------------------------------------------------------------------------------------------------------------------------

#BUAT NGELAYANIN CLIENT
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
       elif ('/upload' in url):
          respon = response_upload(url)
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
        #CLOSE KONEKSI KALO UDAH JENUH, BOSAN, DLL
        koneksi_client.close()


while True:
    #NUNGGU KONEKSI DARI CLIENT, PADAHAL MENUNGGU ITU GAENAK
    print >>sys.stderr, 'waiting for a connection'
    koneksi_client, alamat_client = sock.accept()
    s = threading.Thread(target=layani_client, args=(koneksi_client,alamat_client))
    s.start()