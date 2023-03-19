from telegram.ext import Updater
from telegram.ext import CommandHandler, Filters
from telegram.ext import MessageHandler
import os
from dotenv import load_dotenv

### ai bot ###

import openai
from moviepy.editor import *
import gtts
from playsound import playsound
from PIL import Image
from os import system


load_dotenv()

name = ""
genere = ""
plot = ""
t = 0
pic = 0

def make_video(img, sound, t):
	audio = AudioFileClip(sound)
	clip = ImageClip(img).set_duration(audio.duration)
	clip = clip.set_audio(audio)
	clip.write_videofile("video" + str(t)+".mp4", fps=24)
	
	
def paragraph_generation(script):
	return script.split('\n\n')
	
def to_mp3(paragraph,title):
	tts = gtts.gTTS(paragraph)
	tts.save(title)

print("starting")
KEY = os.getenv('TELE_KEY')
AI_KEY = os.getenv('AI_KEY')

def generate(update, context):
	global name, plot, genere, AI_KEY
	print(name + plot + genere + AI_KEY)
	
	model_engine = "text-davinci-003"
	openai.api_key = AI_KEY	
	prompt = "write me a "
	if genere:
		prompt = prompt + genere + " story "
	else:
		prompt = prompt + "horror story "
	if name:
		prompt = prompt + "about a charachter named " + name + " "
	if plot:
		prompt = prompt + "the plot is " + plot
	 	
	completion = openai.Completion.create(
		engine=model_engine,
		prompt=prompt,
		max_tokens=1024,
		n=1,
		stop=None,
		temperature=0.5,
	) 
	
	response = completion.choices[0].text
	
	update.message.reply_text(response)
	
	global p
	p = paragraph_generation(response)
	
	update.message.reply_text("story is ready, send pictures")

	for i in p:
		if i:
			prompt = "imagine an image that describe this scene " + i + "give me a short description of the image you have imagined"
			completion = openai.Completion.create(
				engine=model_engine,
				prompt=prompt,
				max_tokens=1024,
				n=1,
				stop=None,
				temperature=0.5,
			) 
			res = completion.choices[0].text
			update.message.reply_text("pic"+str(p.index(i))+"\n"+res)
	
def video(update, context):	
	global t 
	global p	
	for i in p:
		if i:
			aud = str(t) + ".mp3"
			image = str(t) + ".jpg"
			to_mp3(i,aud)
			print(aud + " generated")
			make_video(image, aud, t)		
			print("a vid part has been made\n")
			update.message.reply_video(open("video"+str(t)+".mp4"))
			t = t + 1
		
	

def start(update, context):
	update.message.reply_text('hello world')
	
def set_param(update, context):
	user_message = update.message.text
	params =user_message.split('.')
	if params[0] == "name":
		global name
		name = params[1]
		update.message.reply_text(name)
	if params[0] == "genere":
		global genere
		genere = params[1]
		update.message.reply_text(genere)
	if params[0] == "plot":
		global plot
		plot = params[1]
		update.message.reply_text(plot)

def print_param(update, context):
	
	update.message.reply_text("available parametres")
	if plot:
		update.message.reply_text("plot: " + plot)
	if genere:
		update.message.reply_text("genere: " + genere)
	if name:
		update.message.reply_text("name: " + name)

def restart(update, context):
	global name
	name = ""
	global plot
	plot=""
	global t
	t=0
	global pic 
	pic= 0
	global genere
	genere=""		
	system("rm *.mp3 *.mp4 *.jpg")

def save_image(update, context):
	global pic
	file = update.message.photo[0].file_id
	obj = context.bot.get_file(file)
	obj.download(str(pic)+".jpg")
	
	update.message.reply_text("image " +str(pic)+" is saved")
	
	pic = pic + 1


updater = Updater(KEY, use_context=True)
dp = updater.dispatcher

dp.add_handler(CommandHandler("start", start))

dp.add_handler(CommandHandler("print", print_param))
dp.add_handler(CommandHandler("restart", restart))
dp.add_handler(CommandHandler("video",video))
dp.add_handler(CommandHandler("gen", generate))

dp.add_handler(MessageHandler(Filters.text, set_param))
dp.add_handler(MessageHandler(Filters.photo, save_image))

updater.start_polling()

updater.idle()
