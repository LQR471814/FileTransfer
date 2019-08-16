import FileTransfer as ft
import socket
import threading

def AcceptNewClients(s, ClientList, BufferSize):
    while True:
        conn, addr = s.accept()
        ClientList.append(conn)
        NewThread = threading.Thread(target=TransferMessage, kwargs={"s":conn, "ClientList":ClientList, "BufferSize":BufferSize})
        NewThread.start()

def TransferMessage(s, ClientList, BufferSize):
    while True:
        try:
            ReceivedMessages = s.recv(BufferSize)
        except Exception as err:
            print(err)
            return
        for ClientSockt in ClientList:
            if ClientSockt != s:
                try:
                    ClientSockt.send(ReceivedMessages)
                except Exception as ErrSend:
                    print(ErrSend)
                    return

ClientList = []
Buffersize = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("0.0.0.0", 32123))
s.listen(10)

ServerThread = threading.Thread(target=AcceptNewClients, kwargs={"s":s, "ClientList":ClientList, "BufferSize":Buffersize})
ServerThread.daemon = True
ServerThread.start()

ClientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ClientSock.connect(("127.0.0.1", 32123))
print("Connected!")

ft.Receive("C:\\Users\\Sid\\Documents\\Codes\\FTUniversal\\", ClientSock)
while True:
    pass
    