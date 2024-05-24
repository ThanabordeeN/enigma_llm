import threading
import pygame
import logging
import time
from tts.tts import edge2s
from LLM.groq_llm import get_llm_response
from recorder.recorder import AudioRecorder
from disrupt.disrupt import voice_distrupt
from asr.asr import ASR

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class App:
    def __init__(self) -> None:
        self.recorder = AudioRecorder()
        self.asr = ASR()
        self.context = [{"role": "system", "content": "You are my favorite person in the world , always give short conversation."}]
        self.edge2 = edge2s()
        self.disrupt = voice_distrupt()
        self.mixer_flag = threading.Event()  # Flag to signal mixer stop
        self.mixer_flag.set()
        self.audio_playing = False
        self.response = ""

    def main(self):
        self.stop_tts()
        pygame.mixer.init()
        self.mixer_flag.set()
        self.recorder.start_recording()
        text = self.asr.transcribe("HUMAN.wav")
        logging.info(f"Transcribed text: {text}")
        self.context.append({'role': 'user', 'content': text})

        # Stop any existing TTS if it's running
        response = get_llm_response(self.context)
        self.context.append({'role': 'assistant', 'content': response})
        self.response = response
        logging.info(f"Response: {response}")
        self.generate(self.response)

    def generate(self, text):
        """Generates TTS and plays it, checking for stop signal."""
        logging.info("Generating TTS and playing audio")
        try:
            self.audio_playing = True
            self.edge2.speak(text=text)

        except Exception as e:
            logging.info(f"Error during playback: {e}")
        finally:
            self.audio_playing = False

    def stop_tts(self):
        """Stops the TTS thread gracefully."""
        print(self.audio_playing)
        if self.audio_playing:
            pygame.mixer.music.stop()
            pygame.mixer.quit()

    def play_audio(self, filename="AI.mp3"):
        """Plays audio in a non-blocking manner using Pygame's mixer."""
        logging.info("Playing audio")
        try:
            self.audio_playing = True
            pygame.mixer.music.load(filename)
            pygame.mixer.music.play()

            # Check the mixer flag periodically
            while pygame.mixer.music.get_busy():
                if not self.mixer_flag.is_set() & pygame.mixer.music.get_busy():
                    logging.info("Stopping audio")
                    pygame.mixer.music.stop()
                    pygame.mixer.quit()
                    break

            self.audio_playing = False
        except Exception as e:
            logging.info(f"Error playing audio: {e}")
            self.audio_playing = False

    def detect_voice_disrupt(self):
        logging.info("Detecting voice disrupt")
        if self.disrupt.voice_distrupt() and self.audio_playing:
            logging.info("Voice disrupted, stopping audio")
            self.mixer_flag.clear()  # Signal to stop the audio
            logging.info("Audio stopped")

    def run(self):
        while True:
            self.main()
            time.sleep(0.5)
            disrupt_thread = threading.Thread(target=self.detect_voice_disrupt)
            play_thread = threading.Thread(target=self.play_audio)

            disrupt_thread.start()
            play_thread.start()

            disrupt_thread.join()
            play_thread.join()

if __name__ == "__main__":
    app = App()
    app.run()
