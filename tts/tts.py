import edge_tts

class edge2s:
    """Text to speech using Edge TTS API"""
    def __init__(self):
        pass

    def speak(self,text: str , speaker = "en-US-AriaNeural") -> None:
        """
        Convert text to speech using Edge TTS API

        Args:
            text (str): The text to convert to speech.
            speaker (str): The speaker to use for the speech. Defaults to "en-US-AriaNeural".
        
        list of supported voices:
        "Male": "th-TH-NiwatNeural", 
        "Female": "th-TH-PremwadeeNeural"
        "Female": "en-US-AnaNeural", 
        "Female":"en-US-AriaNeural"
        
        and more you can find List of supported voices here:
        https://gist.github.com/BettyJJ/17cbaa1de96235a7f5773b8690a20462
        """
        voice = speaker
        communicate = edge_tts.Communicate(text, voice)
        communicate.save_sync("AI.mp3")
