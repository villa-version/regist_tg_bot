import telebot as tg
import sqlite3
from pprint import pprint
import json


TOKEN = '6532152577:AAFqcSpzFShc2rIYrQUb6zaKxEUqCDHeLls'
bot = tg.TeleBot(TOKEN)
reg_allow = False


#db = sqlite3.connect('users_data.db')
#cur = db.cursor()
#cur.execute("""CREATE TABLE users (
#    login text,
#    password text
#)""")
#db.commit()
#db.close()


@bot.message_handler(commands=['start'])
def start(message):
    markup = tg.types.InlineKeyboardMarkup()
    markup.add(tg.types.InlineKeyboardButton('Да', callback_data='positive'))
    markup.add(tg.types.InlineKeyboardButton('Нет', callback_data='negative'))
    bot_text = 'Здравствуйте {name}. Вы уже зарегистрировались здесь?'.format(name=message.from_user.first_name)
    bot.send_message(message.chat.id, bot_text, reply_markup=markup)


@bot.message_handler(commands=['db'])
def check_db(message):
    db = sqlite3.connect('users_data.db')
    cur = db.cursor()
    cur.execute('SELECT * FROM users')
    text = cur.fetchall()
    pprint(text)
    cur.close()
    db.close()
    #bot.send_message(message.chat.id, json.load(text))


@bot.message_handler()
def register(message):
    global reg_allow
    if reg_allow:
        #try:
        login, password = message.text.split(' ')
        db = sqlite3.connect('users_data.db')
        cur = db.cursor()
        req = f"INSERT INTO users(login, password) VALUES('{login}','{password}')"
        cur.execute(req)
        db.commit()
        cur.close()
        db.close()
        reg_allow = False
        #except Exception:
        #    bot.send_message(message.chat.id, f'Что то пошло не так! Введите еще раз!')


@bot.callback_query_handler(func=lambda callback: True)
def check_callback(callback):
    global reg_allow
    if callback.data == 'positive':
        bot.send_message(callback.message.chat.id, 'Давайте залогинемся! Введите Пожалуйста ваш логин и пароль через пробел.')
    elif callback.data == 'negative':
        reg_allow = True
        bot.send_message(callback.message.chat.id, 'Введите Пожалуйста ваш логин и пароль через пробел.')


bot.infinity_polling()


