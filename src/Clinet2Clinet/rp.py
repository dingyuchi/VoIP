import pyaudio
import speex
import sys

e = speex.Encoder()
e.initialize(speex.SPEEX_MODEID_WB)
d = speex.Decoder()
d.initialize(speex.SPEEX_MODEID_WB)

chunk = 320
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 2

p = pyaudio.PyAudio()

chunklist = []

stream = p.open(format = FORMAT,
                channels = CHANNELS, 
                rate = RATE, 
                input = True,
                output = True,
                frames_per_buffer = chunk)

for i in range(0, 44100 / chunk * RECORD_SECONDS):

    #Encode.
    data = stream.read(chunk)       #Read data from the mic.
    encdata = e.encode(data)        #Encode the data.
    chunklist.append(encdata)       #Record the data in an arbitrary list.

for i in range(len(chunklist)):
    
    decdata = d.decode(chunklist[i])#DECODE my data. (YaY)
    stream.write(decdata, chunk)    #Write the data back out to the speakers

    
stream.stop_stream()
stream.close()
p.terminate()
e.destroy()
d.destroy()
