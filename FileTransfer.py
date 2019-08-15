#------------------------------------------------------#
# Project Name: FileTransfer                           #
# Author: LQR471814                                    #
#------------------------------------------------------#
import socket
import threading
import struct
import platform
import time

def Send(filepath, socket):
    #!Note: Please provide a seperate socket for sending files.
    CurrentPlatform = platform.system()
    if "Windows" == CurrentPlatform:
        Filename = filepath.split("\\")
    if "Darwin" == CurrentPlatform or "Linux" == CurrentPlatform:
        Filename = filepath.split("/")
    Filename = Filename[len(Filename) - 1]
    print(Filename)
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
    try:
        FileContents = FileContents.encode("utf8")
    except:
        pass
    FileLength = len(FileContents) + 4
    bMessageLen = struct.pack("!I", FileLength)

    FilenameMsg = "Filename: -[(-+-)]- " + Filename
    FilenameMsg = FilenameMsg.encode("utf8")
    try:
        socket.send(FilenameMsg)
    except:
        print("ERROR: The socket could not send the message!")
        return

    FileConts = bMessageLen + FileContents
    try:
        socket.send(FileConts)
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
        ReceivedMsg = ""
        msg = ""
        while True:
            try:
                msg = socket.recv(1024) #? Receiving of messages
            except:
                continue
            # try: #? Handling of bytes
            print(msg)
            ReceivedMsg = msg.decode("utf8")
            # except: #? Handling of bytes
                # try:
                #     ReceivedMsg = msg
                #     print("It's bytes")
                # except:
                #     print("Print, Received message is what?")
                # print("Handling Different bytes")
            # try:    
            if "Filename: -[(-+-)]- " in ReceivedMsg: #? Handling of filename
                Name = ReceivedMsg.split("Filename: -[(-+-)]- ")[1]
                continue
            else: #? Handling of file
                print("Handling file")
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
                        print("WRITTEN!")
                        return
            # except:
            #     print("Failed handling filenames")
            
    WorkingThreadFileTrans = threading.Thread(target=worker, kwargs={"destinationpath":destinationpath, "socket":socket})
    WorkingThreadFileTrans.daemon = True
    WorkingThreadFileTrans.start()