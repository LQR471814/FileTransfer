#------------------------------------------------------#
# Project Name: FileTransfer                           #
# Author: LQR471814                                    #
#------------------------------------------------------#
import socket
import threading
import struct
import os

def Send(filepath, socket):
    #!Note: Please provide a seperate socket for sending files.
    Filename = filepath.split("\\")
    Filename = Filename[len(Filename) - 1]
    print(Filename)
    try:
        file = open(filepath, "rb")
    except:
        print("ERROR: Cannot read file! (Are you sure that the file's path is correct?)")
    
    FileContents = file.read()
    try:
        FileContents = FileContents.encode("utf8")
    except:
        pass
    FileLength = len(FileContents) + 4
    bMessageLen = struct.pack("!I", FileLength)

    msg = "Filename: -[(-+-)]- " + Filename
    msg = msg.encode("utf8")
    try:
        socket.send(msg)
    except:
        print("ERROR: The socket could not send the message!")
        return

    msg = bMessageLen + FileContents
    try:
        socket.send(msg)
    except:
        print("ERROR: The socket could not send the message!")
        return
    
def Receive(destinationpath, socket):
    #!Note: Please provide a seperate socket for receiving files.
    def worker(destinationpath, socket):
        Name = ""
        EntireCurrentFile = ""
        FileLen = 0
        CurrentFileLen = 0
        FirstMessage = True
        while True:
            msg = socket.recv(1024) #? Receiving of messages
            
            try: #? Handling of bytes
                ReceivedMsg = msg.decode("utf8")
                
            except: #? Handling of bytes
                ReceivedMsg = msg
                
            if "Filename: -[(-+-)]- " in ReceivedMsg: #? Handling of filename
                Name = ReceivedMsg.split("Filename: -[(-+-)]- ")[1]

            else: #? Handling of file
                if FirstMessage == True:
                    FileLen = struct.unpack("!I", ReceivedMsg[:4])[0]
                    CurrentFileLen = len(ReceivedMsg)
                    EntireCurrentFile = ReceivedMsg[4:]
                else:
                    if FileLen > CurrentFileLen:    
                        CurrentFileLen += len(ReceivedMsg)
                        EntireCurrentFile += ReceivedMsg
                    if FileLen <= CurrentFileLen:
                        NF = open(Name, "wb")
                        NF.write(EntireCurrentFile)
                        NF.close
                        return

    t1 = threading.Thread(target=worker, kwargs={"destinationpath":destinationpath, "socket":socket})
    t1.daemon = True
    t1.start()