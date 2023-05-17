import time
import playsound
from functools import cache
from gtts import gTTS

def speak(text, language):
	tts = gTTS(text, lang=language)
	tts.save("audio.mp3")
	playsound.playsound("./audio.mp3")

def speaker(language, video_to_speaker):

	while True:
		if not video_to_speaker.empty():
			text = video_to_speaker.get()
			speak(text, language)
		time.sleep(0.01)