import pyaudio
import wave
from array import array
import time
import logging
class AudioRecorder:
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 1024
    RECORD_SECONDS = 1
    FILE_NAME = "HUMAN.wav"

    def __init__(self):
        pass
    def start_recording(self):
        audio = pyaudio.PyAudio()
        stream = audio.open(format=self.FORMAT, channels=self.CHANNELS, 
                                 rate=self.RATE, input=True, frames_per_buffer=self.CHUNK ,input_device_index=1)

        frames = []
        start_time = time.time()
        last_sound_time = start_time
        logging.info("recording...")
        while True:
            data = stream.read(self.CHUNK)
            data_chunk = array('h', data)
            vol = max(data_chunk)
            if vol >= 500:
                logging.info("🔊")
                frames.append(data)
                last_sound_time = time.time()
            else:
                logging.info("🔇")

            if time.time() - start_time > self.RECORD_SECONDS and time.time() - last_sound_time > 1:
                if len(frames) > 10:
                    break

        stream.stop_stream()
        stream.close()
        audio.terminate()
        self.save_to_file(frames,audio)

    def save_to_file(self, frames,audio):
        wavfile = wave.open(self.FILE_NAME, 'wb')
        wavfile.setnchannels(self.CHANNELS)
        wavfile.setsampwidth(audio.get_sample_size(self.FORMAT))
        wavfile.setframerate(self.RATE)
        wavfile.writeframes(b''.join(frames))
        wavfile.close()
  
            
        
# Usage
