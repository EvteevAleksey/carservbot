import telebot
import sys
import time
import json
import psycopg2

config = None
with open('config.json', 'r') as F:
    config = json.loads(F.read())
TOKEN = config['telegram']['token']
bot = telebot.TeleBot(TOKEN)
with psycopg2.connect(
                "dbname='%(name)s' user='%(login)s' host='%(ip)s' password='%(password)s'" % config['db']
) as db:
    db.autocommit = True


class DBLayer:
    def __init__(self, db):
        self._db = db

    def getState(self, uid):
        with self._db.cursor() as cursor:
            cursor.execute("""
                SELECT state FROM chats1 WHERE uid = %s LIMIT 1
                """, [uid])

            if cursor.rowcount == 1:
                state, = cursor.fetchone()
                return state
            else:
                return {}
        return None


    def getUserBrand(self, uid):
        with self._db.cursor() as cursor:
            cursor.execute("""
                SELECT user_brand FROM chats1 WHERE uid = %s LIMIT 1
                """, [uid])

            if cursor.rowcount == 1:
                state, = cursor.fetchone()
                if state == 'null':
                    return None
                else:
                    return state
            else:
                return None
        return None


    def getBrand(self, message):
        with self._db.cursor() as cursor:
            cursor.execute("""
                select Auto_name
                from Brand, plainto_tsquery(%s) as query
                where to_tsvector(Brand_name) @@ query = true
                """, [message.lower()])
            if cursor.rowcount == 1:
                str, = cursor.fetchone()
                return str
            else:
                return None


    def updateState(self, uid, new_state):
        with self._db.cursor() as cursor:
            cursor.execute("""
                INSERT INTO chats1 (uid, state) VALUES (%(uid)s, %(new_state)s)
                ON CONFLICT (uid)
                DO UPDATE
                SET state = %(new_state)s,
                updated_at = now()
                """, {'uid': uid, 'new_state': json.dumps(new_state)})

    def updateBrand(self, uid, new_brand):
        with self._db.cursor() as cursor:
            cursor.execute("""
                INSERT INTO chats1 (uid, user_brand) VALUES (%(uid)s, %(new_brand)s)
                ON CONFLICT (uid)
                DO UPDATE
                SET user_brand = %(new_brand)s,
                updated_at = now()
                """, {'uid': uid, 'new_brand': new_brand})


DB = DBLayer(db)
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
