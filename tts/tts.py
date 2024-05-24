import edge_tts

class edge2s:
    """Text to speech using Edge TTS API"""
    def __init__(self):
        pass

    def speak(self,text: str) -> None:
        """
        Convert text to speech using Edge TTS API

        Args:
            text (str): Text to speech
            gender (str): Male or Female (default: Male)
        """
        #voice_map = {"Male": "th-TH-NiwatNeural", "Female": "th-TH-PremwadeeNeural"}
        #voice = voice_map.get(gender, "th-TH-NiwatNeural")  # default to Male voice
        voice = "en-US-AnaNeural"
        communicate = edge_tts.Communicate(text, voice,pitch = "-15Hz")
        communicate.save_sync("AI.mp3")
