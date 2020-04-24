import socket
import FileTransfer as ft

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1", 32123))

ft.send("file", s)