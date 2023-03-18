import openai
import gtts
from playsound import playsound

def paragraph_generation(script):
	return script.split('\n\n')

def to_mp3(paragraph,title):
	tts = gtts.gTTS(paragraph)
	tts.save(title)

openai.api_key = "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"
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

p = paragraph_generation(response)
t = 0

for i in p:
	if i:
		to_mp3(i,str(t) + ".mp3")
		t = t + 1
