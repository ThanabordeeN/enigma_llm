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
    def voice_distrupt(self, volume=1000 ,sentivity=7) -> bool:
        """
        Records audio from the default input device and detects disruptive sound events.

        Args:
            volume (int): The minimum volume threshold to consider a sound event as disruptive. Default is 1000.
            sentivity (int): The number of consecutive disruptive sound events required to trigger a detection. Default is 7.

        Returns:
            bool: True if a disruptive sound event is detected, False otherwise.
        """
        audio = pyaudio.PyAudio()
        stream = audio.open(format=FORMAT, channels=CHANNELS, 
                            rate=RATE, input=True, frames_per_buffer=CHUNK, input_device_index=1)

        logging.info("recording...")
        while True:
            data = stream.read(CHUNK)
            data_chunk = array('h', data)
            vol = max(data_chunk)
            if vol >= volume:
                logging.info("🔊")
                self.distrupt.append(data)
                if len(self.distrupt) > sentivity:
                    break
            else:
                logging.info("🤫")
        stream.stop_stream()
        stream.close()  
        audio.terminate()
        self.distrupt = []
        return True
    