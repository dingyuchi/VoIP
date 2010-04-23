# -*- coding: utf-8 -*-
from pyaudio import paInt16
import pyaudio
import speex
import socket
import time

d = speex.Decoder()
d.initialize(speex.SPEEX_MODEID_WB)

host = ''
port = 20000
ADDR = (host,port)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))

# stream output
FRAME_SIZE = 320        # FRAME大小
SAMPLING_RATE = 8000    # 取樣頻率
p = pyaudio.PyAudio()
streamout = p.open(format=paInt16,
                   channels=1,
                   rate=SAMPLING_RATE,
                   output=True)
start = time.clock()
rate = 0
while True:
    buf, address = s.recvfrom(1024)
    rate = rate + len(buf)
    print "Got data From:", address, "Size:", rate/(time.clock() - start) 
    decdata = d.decode(buf)
    streamout.write(decdata)

# control
streamout.close()
p.terminate()
