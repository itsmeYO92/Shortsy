import openai
from moviepy.editor import *
import gtts
from playsound import playsound
from craiyon import Craiyon
import os
from dotenv import load_dotenv
from PIL import Image
from os import system
load_dotenv()


generator = Craiyon()

def make_video(img, sound, t):
	audio = AudioFileClip(sound)
	clip = ImageClip(img).set_duration(audio.duration)
	clip = clip.set_audio(audio)
	clip.write_videofile("video" + str(t)+".mp4", fps=24)

	
	

def generate_image(text):
	result = generator.generate(text)
	result.save_images()


def paragraph_generation(script):
	return script.split('\n\n')

def to_mp3(paragraph,title):
	tts = gtts.gTTS(paragraph)
	tts.save(title)

openai.api_key = os.getenv('KEY')
model_engine = "text-davinci-003"

genre=input("Whats your genre: ")
prompt = "write me a " + genre + "story"

completion = openai.Completion.create(
	engine=model_engine,
	prompt=prompt,
	max_tokens=1024,
	n=1,
	stop=None,
	temperature=0.5,
) 

response = completion.choices[0].text

print("stroy has been generated:      ")

p = paragraph_generation(response)
print("story is ready")

t = 0

for i in p:
	if i:
		aud = str(t) + ".mp3"
		image = str(t) + ".png"
		to_mp3(i,aud)
		print(aud + " generated")
		generate_image(i)
		print(image + " generated")
		im = Image.open("generated/image-1.webp").convert("RGB")
		im.save(image,"png")
		make_video(image, aud, t)		
		print("a vid part has been made\n")

		t = t + 1
