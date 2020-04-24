import random

fObj = open("file", "wb")
for i in range(1000000):
    fObj.write(chr(random.randint(0, 2000)).encode("utf8"))
