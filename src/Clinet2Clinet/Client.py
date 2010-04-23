# -*- coding: utf-8 -*-
from pyaudio import PyAudio, paInt16
from speex import SPEEX_SET_QUALITY
from threading import Thread
import pyaudio
import socket
import speex
from Queue import Queue

# speex
e = speex.Encoder()
e.initialize(speex.SPEEX_MODEID_WB)
d = speex.Decoder()
d.initialize(speex.SPEEX_MODEID_WB)

# buffer
q = Queue()

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
host = "127.0.0.1"
outport = 20000
outADDR = (host,outport)
s1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

inport = 20002
inADDR = ('0.0.0.0', inport)
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
        buf, address = s2.recvfrom(1024)
        q.put(buf) 
        if q.empty() == False:
            decdata = d.decode(q.get())
            streamout.write(decdata)

t2 = Thread(target=OutputToSpeaker)
t2.start()

# control
def BitRate():
    while True:
        quality=input('Please enter a quality [0-10]:')
        e.control(SPEEX_SET_QUALITY, int(quality))

t3 = Thread(target=BitRate)
t3.start()

while True:
    buf, address = s2.recvfrom(1024)
    print "Got data from:", address, "Size:", len(buf)
    decdata = d.decode(buf)
    streamout.write(decdata)

streamin.close()
pa.terminate()
streamout.close()
p.terminate()
