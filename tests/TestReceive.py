import socket
import FileTransfer as ft

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("0.0.0.0", 32123))
s.listen(1)
conn, addr = s.accept()

result = ft.receive("C:\\destination\\folder\\path\\", conn)
print("Filename: ", result[1], "File Contents: ", result[0])