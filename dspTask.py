import telebot
import requests
import string
import datetime
from peewee import *
from botdb import *

db = SqliteDatabase(
    'bot.db'
)
db.connect()

API_TOKEN = '835807348:AAEqPZLPjIkzeFK-1p1zG7N7YKtAzUvbzkE'
exclude = set(string.punctuation+' ')
            
bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    uid = message.from_user.id
    User.insert(uid=uid).execute()
    bot.reply_to(message, "Hello. Feed me a voice message")
    
@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message, "I eat voice messages")

@bot.message_handler(content_types=["voice"])
def save_voice(message):
    uid = message.from_user.id
    file_id = message.voice.file_id
    file_info = bot.get_file(file_id)
    file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(API_TOKEN, file_info.file_path))
    
    s = ''.join(ch for ch in str(datetime.datetime.now()) if ch not in exclude)+'.ogg'
    with open(s, 'wb') as f:
        f.write(file.content)        
    Voice.insert(path=s, user=uid).execute()
    
    bot.reply_to(message, 'message saved')

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, 'Feed me a voice message')

bot.polling(none_stop=False, timeout=30)