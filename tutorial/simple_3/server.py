#server.py
 
import sys
import socket
import os
 
host = ''
skServer = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
skServer.bind((host,2525))
skServer.listen(10)
print "Server Active"
bFileFound = 0
 
while True:
    Content,Address = skServer.accept()
    print Address
    sFileName = Content.recv(1024)
    for file in os.listdir("files/"):
        if file == sFileName:
            bFileFound = 1
            break
 
    if bFileFound == 0:
        print sFileName+" Not Found On Server"
 
    else:
        print sFileName+" File Found"
        fUploadFile = open("files/"+sFileName,"rb")
        sRead = fUploadFile.read(1024)
        while sRead:
            Content.send(sRead)
            sRead = fUploadFile.read(1024)
        print "Sending Completed"
    break
 
Content.close()
skServer.close()
