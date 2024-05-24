from transformers import pipeline
class ASR:
    def __init__(self):
        self.pipe = pipeline(
            task="automatic-speech-recognition",
            model="openai/whisper-small",
            device=0,
            chunk_length_s=30,
        )
    def transcribe(self, speech_file):
        return self.pipe(speech_file, generate_kwargs = {"task":"transcribe", "language":"english"})['text']
    
    
