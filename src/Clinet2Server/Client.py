# -*- coding: utf-8 -*-
from pyaudio import PyAudio, paInt16
from speex import SPEEX_SET_QUALITY
from threading import Thread
import speex
import socket, sys
from speex import SPEEX_SET_VBR

e = speex.Encoder()
e.initialize(speex.SPEEX_MODEID_WB)

# stream input
FRAME_SIZE = 320        # FRAME大小
SAMPLING_RATE = 8000    # 取樣頻率
pa = PyAudio() 
streamin = pa.open(format=paInt16,
                   channels=1,
                   rate=SAMPLING_RATE,
                   input=True,
                   frames_per_buffer=FRAME_SIZE) 

host = "140.119.164.20"
port = 20000
ADDR = (host,port)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# play
def InputFromMIC():
    while True:
        string_audio_data = streamin.read(FRAME_SIZE)   
        encdata = e.encode(string_audio_data)
        s.sendto(encdata,ADDR)   
        
t1 = Thread(target=InputFromMIC)
t1.start()

# control
while True:
    quality=input('Please enter a quality [0-10]:')
    e.control(SPEEX_SET_QUALITY, int(quality))

streamin.close()
pa.terminate()
