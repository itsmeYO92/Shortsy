import gtts
from playsound import playsound

def to_mp3(paragraph,title):
	tts = gtts.gTTS(paragraph)
	tts.save(title)


p = "lskfglksf"
t = 1

to_mp3(p, str(t) + "test.mp3")

