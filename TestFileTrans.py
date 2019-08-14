import FileTransfer as ft
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("192.168.1.144", 32123))
print("Connected")
ft.Send(filepath="~/Downloads/FileTransfer-master/README.md", socket=s)