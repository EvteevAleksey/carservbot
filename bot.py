import telebot
import sys
import DB
import config
import createdb
bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['start'])
def start(message):
    if db.getUserBrand(message.chat.id) is None:
        sent = bot.send_message(message.chat.id,"Выберите тип вопроса \n\n1. Поиск детали \n2. Вопрос по ремонту \n3. Обслуживание \n4. ТО")
        bot.register_next_step_handler(sent,reply2)
    else:
        sent = bot.send_message(message.chat.id, 'Какая марка?')
        bot.register_next_step_handler(sent, reply1)

def reply1(message):
    Brand = db.getBrand(message.text)
    if Brand is not None:
        sent = bot.send_message(message.chat.id, "Окей, у вас %s" % Brand)
        db.updateBrand(message.chat.id, Brand)
        bot.register_next_step_handler(sent,reply2)
    else:
        sent = bot.send_message("Не удалось распознать марку автомобиля")
        bot.register_next_step_handler(sent,reply1)


def reply2(message):
    bot.send_message(message.chat.id, '{name}. Заканчивай.'.format(name=message.text))




if __name__ == '__main__':
    createdb.createtables()
    db = DB.DBLayer(config.database)
    while True:
            try:
                bot.polling(none_stop=True,interval=5)
            except Exception as e:
                print('Error occurred:')
                print(sys.stderr, str(e))