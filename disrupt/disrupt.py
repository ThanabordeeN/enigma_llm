import pyaudio
from array import array
import logging
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
class voice_distrupt:
    def __init__(self):
        self.distrupt = []
    def voice_distrupt(self):
        audio = pyaudio.PyAudio()
        stream = audio.open(format=FORMAT, channels=CHANNELS, 
                                    rate=RATE, input=True, frames_per_buffer=CHUNK ,input_device_index=1)

        logging.info("recording...")
        while True:
            data = stream.read(CHUNK)
            data_chunk = array('h', data)
            vol = max(data_chunk)
            if vol >= 1000:
                logging.info("🔊")
                self.distrupt.append(data)
                if len(self.distrupt) > 10:
                    break
            else:
                logging.info("🤫")
        stream.stop_stream()
        stream.close()  
        audio.terminate()
        self.distrupt = []
        return True
    