import threading
import pygame
import logging
from tts.tts import edge2s
from LLM.groq_llm import get_llm_response
from recorder.recorder import AudioRecorder
from disrupt.disrupt import voice_distrupt
from asr.asr import ASR

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class App:
    """
    Main application class for handling audio recording, transcription, and text-to-speech generation.
    """    
    def __init__(self) -> None:
        """
        Initializes the App with necessary components for audio handling and conversation context.
        """
        self.recorder = AudioRecorder()
        self.asr = ASR()
        self.context = [{"role": "system", "content": "You are my favorite person in the world , we have common short conversation."}]
        self.edge2 = edge2s()
        self.disrupt = voice_distrupt()
        self.mixer_flag = threading.Event()  # Flag to signal mixer stop
        self.mixer_flag.set()
        self.audio_playing = False
        self.response = ""

    def main(self):
        """
        Main function to handle the recording, transcription, and response generation process.
        """
        self.stop_tts()
        pygame.mixer.init()
        self.mixer_flag.set()
        self.recorder.start_recording()
        text = self.asr.transcribe(speech_file="HUMAN.wav", language="english") 
        logging.info(f"Transcribed text: {text}")
        self.context.append({'role': 'user', 'content': text})

        # Stop any existing TTS if it's running
        response = get_llm_response(self.context)
        self.context.append({'role': 'assistant', 'content': response})
        self.response = response
        logging.info(f"Response: {response}")
        self.generate(self.response)

    def generate(self, text):
        """
        Generates Text-to-Speech (TTS) and plays it. 

        Args:
            text (str): The text to be converted to speech.

        Raises:
            Exception: If there's an error during playback.
        """
        logging.info("Generating TTS and playing audio")
        try:
            self.audio_playing = True
            self.edge2.speak(text=text,speaker = "en-US-AriaNeural") # Generate TTS

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
        """
        Plays audio in a non-blocking manner using Pygame's mixer.

        Args:
            filename (str, optional): The name of the audio file to be played. Defaults to "AI.mp3".

        Raises:
            Exception: If there's an error during audio playback.
        """
        logging.info("Playing audio")
        try:
            self.audio_playing = True
            pygame.mixer.music.load(filename)
            pygame.mixer.music.play()
            # Check the mixer flag periodically
            while pygame.mixer.music.get_busy():
                if not self.mixer_flag.is_set() :
                    logging.info("Audio stopped by user")
                    pygame.mixer.music.stop()
                    pygame.mixer.quit()
                    
            logging.info("Audio finished playing")
            self.audio_playing = False
            pygame.mixer.music.stop()
            pygame.mixer.quit()
        except Exception as e:
            logging.info(f"Error playing audio: {e}")
            self.audio_playing = False
            

    def detect_voice_disrupt(self):
        """
        Detects voice disruption and stops the audio if it's currently playing.
        """
        logging.info("Detecting voice disrupt")
        if self.disrupt.voice_distrupt(volume=1000) and self.audio_playing:
            logging.info("Voice disrupted, stopping audio")
            self.mixer_flag.clear()  # Signal to stop the audio
            logging.info("Audio stopped")

    def run(self):
        """
        Runs the main application loop, continuously recording, transcribing, and responding to user input.
        """
        while True:
            self.main()
            disrupt_thread = threading.Thread(target=self.detect_voice_disrupt)
            play_thread = threading.Thread(target=self.play_audio)

            disrupt_thread.start()
            play_thread.start()

            disrupt_thread.join()
            play_thread.join()

if __name__ == "__main__":
    """
    Entry point of the application.
    """
    app = App()
    app.run()
