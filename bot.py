import telebot
import sys
import time

TOKEN = '529413272:AAGPFw8xASCkvhY-9rqhqtVAmIFaRnrb0go'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    sent = bot.send_message(message.chat.id, 'Как тебя зовут?')
    bot.register_next_step_handler(sent, hello)

def hello(message):
    bot.send_message(message.chat.id, 'Привет, {name}. Рад тебя видеть.'.format(name=message.text))

while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print('Error occurred:')
            print(sys.stderr, str(e))
