# -*- coding: utf-8 -*-
from Queue import Queue
from pyaudio import PyAudio, paInt16
from speex import SPEEX_SET_QUALITY
from threading import Thread
import pyaudio
import speex

e = speex.Encoder()
e.initialize(speex.SPEEX_MODEID_WB)
d = speex.Decoder()
d.initialize(speex.SPEEX_MODEID_WB)

FRAME_SIZE = 320        # FRAME大小
SAMPLING_RATE = 8000    # 取樣頻率

# stream input
pa = PyAudio() 
streamin = pa.open(format=paInt16,
                   channels=1,
                   rate=SAMPLING_RATE,
                   input=True,
                   frames_per_buffer=FRAME_SIZE) 

# stream output
p = pyaudio.PyAudio()
streamout = p.open(format=paInt16,
                   channels=1,
                   rate=SAMPLING_RATE,
                   output=True)

# buffer
q = Queue()

# play
def InputFromMIC():
    while True:
        string_audio_data = streamin.read(FRAME_SIZE)   
        encdata = e.encode(string_audio_data)
        q.put(encdata)   
        
t1 = Thread(target=InputFromMIC)
t1.start()



def OutputToSpeaker():
    while True:  
        if q.empty() == False:
            decdata = d.decode(q.get())
            streamout.write(decdata)

t2 = Thread(target=OutputToSpeaker)
t2.start()

# control
while True:
    quality=input('Please enter a quality [0-10]:')
    e.control(SPEEX_SET_QUALITY, int(quality))

streamin.close()
streamout.close()
pa.terminate()
p.terminate()

