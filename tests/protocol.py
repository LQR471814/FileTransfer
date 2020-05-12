import struct
import random

msg = ""
for i in range(100):
    msg += chr(random.randint(0, 255))

filename = "random.txt"
bFilenameLen = struct.pack("!I", len(filename))
bMsgLen = struct.pack("!I", len(msg))
bMessage = bFilenameLen + filename.encode("utf8") + bMsgLen + msg.encode("utf8")

filenameLen = struct.unpack("!I", bMessage[:4])
filenameDecoded = bMessage[4:filenameLen[0]].decode("utf8")
msgLen = struct.unpack("!I", bMessage[4 + filenameLen[0]:4 + filenameLen[0] + 4])
msgDecoded = bMessage[4 + filenameLen[0] + 4:4 + filenameLen[0] + 4 + msgLen[0]].decode("utf8")

print(filenameLen[0], filenameDecoded, msgLen, msgDecoded)