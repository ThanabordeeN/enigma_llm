# AI Voice Assistant 

## Description

This is an AI voice assistant application that combines audio recording, speech recognition, text-to-speech synthesis, and large language model (LLM) response generation. It also includes a voice disruption detection feature to ensure a seamless user experience. The application is designed to be user-friendly and easy to interact with. 

## Installation

To install the required dependencies, navigate to the project folder and run the following command:

```batch
pip install -r requirements.txt
```

## Usage

To launch the AI voice assistant, simply run the following command:

```batch
python main.py
```

## Components

- **pygame**: Used for audio playback and control. : https://github.com/pygame/pygame
- **groq**: Thank you to the developers of groq for providing fast inference, which is essential for experimental features.
- **pyaudio**: Handles audio recording and input capture.
- **edge_tts**: A text-to-speech synthesis library for converting text responses into spoken words. :https://github.com/rany2/edge-tts.git
- **transformers**: Provides powerful large language models for generating intelligent and contextually appropriate responses.

## Code Breakdown

### Class: App

#### Attributes:

- `recorder`: An instance of the `AudioRecorder` class, responsible for capturing audio input using `pyaudio`.

   ```python
   self.recorder = AudioRecorder()
   ```

- `asr`: An instance of the `ASR` class, used for transcribing recorded audio into text.

   ```python
   self.asr = ASR()
   ```

- `context`: A list of dictionaries representing the conversation context. Each dictionary contains the "role" ("system", "user", or "assistant") and the associated "content" (text).

   ```python
   self.context = [{"role": "system", "content": "Hello! I'm your friendly AI assistant. How can I help you today?"}]
   ```

- `edge2`: An instance of the `edge_tts` class, used for converting text responses into speech.

   ```python
   self.edge2 = edge_tts(speaker = "en-US-AriaNeural")
   ```

- `disrupt`: An instance of the `voice_disrupt` class, responsible for detecting voice disruptions during playback.

   ```python
   self.disrupt = voice_disrupt()
   ```

- `mixer_flag`: A threading.Event flag used to control the Pygame mixer's audio playback.

   ```python
   self.mixer_flag = threading.Event()
   self.mixer_flag.set()
   ```

- `audio_playing`: A boolean flag indicating whether audio playback is currently active.

   ```python
   self.audio_playing = False
   ```

- `response`: A string variable to store the generated response from the LLM.

   ```python
   self.response = ""
   ```

#### Methods:

- `__init__(self) -> None`:
   - Initializes all the attributes mentioned above.
   - Sets the initial state of the `mixer_flag` and `audio_playing` flag.

   ```python
   def __init__(self) -> None:
       self.recorder = AudioRecorder()
       self.asr = ASR()
       self.context = [{"role": "system", "content": "Initial context..."}]
       self.edge2 = edge_tts()
       self.disrupt = voice_disrupt()
       self.mixer_flag = threading.Event()
       self.mixer_flag.set()
       self.audio_playing = False
       self.response = ""
   ```

- `main(self)`:
   - Stops any ongoing TTS playback.
   - Initializes Pygame's mixer for audio output.
   - Starts audio recording and captures user input using `pyaudio`.
   - Transcribes the recorded audio and stores the text.
   - Appends the transcribed text to the `context` list as a user input.
   - Generates an LLM response based on the conversation context.
   - Calls `self.generate(self.response)` to play the response using `edge_tts`.

   ```python
   def main(self):
       self.stop_tts()
       pygame.mixer.init()
       self.mixer_flag.set()
       self.recorder.start_recording(activate_volume=500)
       text = self.asr.transcribe("HUMAN.wav")
       logging.info(f"Transcribed text: {text}")
       self.context.append({'role': 'user', 'content': text})
       response = get_llm_response(self.context)
       self.context.append({'role': 'assistant', 'content': response})
       self.response = response
       logging.info(f"Response: {response}")
       self.generate(self.response)
   ```

- `generate(self, text)`:
   - Generates TTS for the given text and plays the audio using `edge_tts`.
   - Handles exceptions during playback and logs any errors.
   - Updates the `audio_playing` flag accordingly.

   ```python
   def generate(self, text):
       logging.info("Generating TTS and playing audio")
       try:
           self.audio_playing = True
           self.edge2.speak(text,speaker = "en-US-AriaNeural")
       except Exception as e:
           logging.info(f"Error during playback: {e}")
       finally:
           self.audio_playing = False
   ```

- `stop_tts(self)`:
   - Checks the `audio_playing` flag and stops TTS playback if necessary.
   - Quits the Pygame mixer to release audio resources.

   ```python
   def stop_tts(self):
       if self.audio_playing:
           pygame.mixer.music.stop()
           pygame.mixer.quit()
   ```

- `play_audio(self, filename="output.mp3")`:
   - Plays the specified audio file in a non-blocking manner using Pygame.
   - Periodically checks the `mixer_flag` to allow for stopping the audio.
   - Updates the `audio_playing` flag accordingly.
   - Handles exceptions during playback and logs any errors.

   ```python
   def play_audio(self, filename="AI.mp3"):
       logging.info("Playing audio")
       try:
           self.audio_playing = True
           pygame.mixer.music.load(filename)
           pygame.mixer.music.play()
           while pygame.mixer.music.get_busy():
               if not self.mixer_flag.is_set():
                   logging.info("Audio stopped by user")
                   pygame.mixer.music.stop()
                   pygame.mixerSUh.quit()
           logging.info("Audio finished playing")
       except Exception as e:
           logging.info(f"Error playing audio: {e}")
           self.audio_playing = False
   ```

- `detect_voice_disrupt(self)`:
   - Detects voice disruption during audio playback.
   - If voice disruption is detected and audio is playing, it stops the playback.

   ```python
   def detect_voice_disrupt(self):
       logging.info("Detecting voice disrupt")
       if self.disrupt.voice_disrupt(volume=1000) and self.audio_playing:
           logging.info("Voice disrupted, stopping audio")
           self.mixer_flag.clear()
   ```

- `run(self)`:
   - The main loop of the application.
   - Continuously processes user input, generates responses, and plays them back.
   - Spawns threads for voice disruption detection and audio playback.
   - Ensures that the threads complete before continuing the loop.

   ```python
   def run(self):
       while True:
           self.main()
           disrupt_thread = threading.Thread(target=self.detect_voice_disrupt)
           play_thread = threading.Thread(target=self.play_audio)
           disrupt_thread.start()
           play_thread.start()
           disrupt_thread.join()
           play_thread.join()
   ```

## Notes: 

This AI voice assistant demonstrates the power of combining various components like Pygame, groq, pyaudio, edge_tts, and transformers to create an interactive and responsive system. 

We are especially grateful to the developers of groq for providing fast inference, which is crucial for experimental features and enhancing the overall user experience. 

Feel free to explore and customize the code to your liking!