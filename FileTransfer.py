#------------------------------------------------------#
# Project Name: FileTransfer                           #
# Author: LQR471814                                    #
#------------------------------------------------------#
import socket
import threading
import struct
import time
import os

def Send(filepath, socket):
    #!Note: Please provide a seperate socket for sending files.
    #process file name
    Filename = os.path.basename(filepath)
    print("----------->",Filename)
    Filename_bytes = Filename.encode("utf-8")
    FNLen = len(Filename_bytes)
    bMessageLen = struct.pack("!I", FNLen)
    FinMsg = bMessageLen + Filename_bytes
    try:
        socket.send(FinMsg)
    except:
        print("ERROR: The socket could not send the message!")
        return

    #process file content
    try:
        file = open(filepath, "rb")
    except:
        print("ERROR: Cannot open file! (Are you sure that the file's path is correct?)")
        return
    try:
        FileContents = file.read()
    except:
        print("ERROR: Cannot read file! (Are you sure that your directory is a file or file isn't corrupted?)")
        return

    FileLength = len(FileContents)
    bMessageLen = struct.pack("!I", FileLength)
    print("File content length is" ,str(bMessageLen), FileLength)
    FileConts = bMessageLen + FileContents
    try:
        socket.send(FileConts)
    except:
        print("ERROR: The socket could not send the message!")
        return
    
def Receive(destinationpath, socket):
    #!Note: Please provide a seperate socket for receiving files.
    def worker(destinationpath, socket):
        Filename = ""
        EntireCurrentFile = ""
        FileLen = 0
        CurrentFileLen = 0
        FirstMessage = True

        msg = socket.recv(4)
        FNLen = struct.unpack("!I", msg)[0]
        while True:
            msg = socket.recv(1024) #? Receiving of messages
            print(FileLen, "<-- Entire File Length", CurrentFileLen, "<-- Current Packets received length")
            if FirstMessage == True:
                # print(msg[FNLen:FN])
                print(msg[:FNLen])
                Filename = msg[:FNLen - 4].decode("utf8")
                FileLen = struct.unpack("!I", msg[FNLen - 4:FNLen])[0]
                FileLen = FileLen - 8
                FileLen = FileLen - len(Filename)
                CurrentFileLen = len(msg[FNLen:])
                EntireCurrentFile = msg[FNLen:]
                FirstMessage = False
            else:
            # print(b"RandomF".decode("utf8"))
            # print(msg)
            # print(msg[4:FNLen], "Filename")
            # except:
            #     print("Failed handling fiprint(EntireCurrentFile, "EntireCurrentFile")
                if FileLen > CurrentFileLen:
                    CurrentFileLen += len(msg)
                    EntireCurrentFile += msg
                if FileLen <= CurrentFileLen:
                    print("Writing!")
                    NF = open(Filename, "wb")
                    NF.write(EntireCurrentFile)
                    NF.close()
                    # print("definitely")
                    time.sleep(3)
                    print("Done!")
                    
    WorkingThreadFileTrans = threading.Thread(target=worker, kwargs={"destinationpath":destinationpath, "socket":socket})
    # WorkingThreadFileTrans.daemon = True
    WorkingThreadFileTrans.start()