from telegram.ext import Updater
from telegram.ext import CommandHandler
import os
from dotenv import load_dotenv


load_dotenv()

KEY = os.getenv('TELE_KEY')
def start(update, context):
	update.message.reply_text('hello world')


updater = Updater(KEY, use_context=True)
dp = updater.dispatcher

dp.add_handler(CommandHandler("hello", start))

updater.start_polling()

updater.idle()
