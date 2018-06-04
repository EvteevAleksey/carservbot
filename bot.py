import telebot
import sys
import DB
import config
config = None
TOKEN = config.token
bot = telebot.TeleBot(TOKEN)

DB = DB.DBLayer(config.database)
@bot.message_handler(commands=['start'])
def start(message):
    current_state = DB.getstate(message.chat.id)
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
