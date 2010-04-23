# -*- coding: utf-8 -*-
from pyaudio import PyAudio, paInt16
import pyaudio
import speex
import socket
from threading import Thread

# speex
e = speex.Encoder()
e.initialize(speex.SPEEX_MODEID_WB)
d = speex.Decoder()
d.initialize(speex.SPEEX_MODEID_WB)

# stream input/output
FRAME_SIZE = 320        # FRAME大小
SAMPLING_RATE = 8000    # 取樣頻率
pa = PyAudio() 
streamin = pa.open(format=paInt16,
                   channels=1,
                   rate=SAMPLING_RATE,
                   input=True,
                   frames_per_buffer=FRAME_SIZE) 

p = pyaudio.PyAudio()
streamout = p.open(format=paInt16,
                   channels=1,
                   rate=SAMPLING_RATE,
                   output=True)

# socket
host = "192.168.0.216"
outport = 20002
outADDR = (host,outport)
s1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

inport = 20000
inADDR = ("0.0.0.0", inport)
s2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s2.bind(inADDR)

# play
def InputFromMIC():
    while True:
        string_audio_data = streamin.read(FRAME_SIZE)   
        encdata = e.encode(string_audio_data)
        s1.sendto(encdata,outADDR)   
        
t1 = Thread(target=InputFromMIC)
t1.start()

def OutputToSpeaker():
    while True:  
        buf,address = s2.recvfrom(1024)
        decdata = d.decode(buf)
        streamout.write(decdata)

t2 = Thread(target=OutputToSpeaker)
t2.start()

while True:
    buf, address = s2.recvfrom(1024)
    print "Got data from:", address, "Size:", len(buf)
    decdata = d.decode(buf)
    streamout.write(decdata)

# control
streamout.close()
p.terminate()
