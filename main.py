import telebot as tg
import sqlite3


TOKEN = '6532152577:AAFqcSpzFShc2rIYrQUb6zaKxEUqCDHeLls'
bot = tg.TeleBot(TOKEN)
reg_allow = False
log_allow = False


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


@bot.message_handler(commands=['cleardb'])
def clear_db(message):
    try:
        _, login, password = message.text.split(' ')
        req = f'DELETE FROM users WHERE login="{login}" AND password="{password}"'
    except ValueError:
        req = 'DELETE FROM users'
    db = sqlite3.connect('users_data.db')
    cur = db.cursor()
    cur.execute(req)
    db.commit()
    cur.close()
    db.close()


@bot.message_handler(commands=['db'])
def check_db(message):
    db = sqlite3.connect('users_data.db')
    cur = db.cursor()
    cur.execute('SELECT * FROM users')
    text = cur.fetchall()
    cur.close()
    db.close()
    msg = 'LIST OF USERS DATA\n'
    for ud in text:
        msg += '{log}: {psswrd}\n'.format(log=ud[0], psswrd=ud[1])
    bot.send_message(message.chat.id, msg)


@bot.message_handler()
def account_operations(message):
    global reg_allow, log_allow
    if reg_allow:
        try:
            login, password = message.text.split(' ')
            reg_allow = False
        except ValueError:
            bot.send_message(message.chat.id, f'Вы ввели не верно! Введите еще раз! (Через пробел)')
            return
        db = sqlite3.connect('users_data.db')
        cur = db.cursor()
        req = f"INSERT INTO users(login, password) VALUES('{login}','{password}')"
        cur.execute(req)
        db.commit()
        cur.close()
        db.close()
        bot.send_message(message.chat.id, 'Поздравляю! Вы вошли в систему успешно!')
    elif log_allow:
        try:
            login, password = message.text.split(' ')
        except ValueError:
            bot.send_message(message.chat.id, f'Вы ввели не верно! Введите еще раз! (Через пробел)')
            return
        db = sqlite3.connect('users_data.db')
        cur = db.cursor()
        cur.execute('SELECT * FROM users')
        text = cur.fetchall()
        db.commit()
        cur.close()
        db.close()
        for ud in text:
            if ud[0] == login and ud[1] == password:
                log_allow = False
                break
            if text.index(ud) == len(text)-1:
                bot.send_message(message.chat.id, 'Не удалось войти в систему. Вы ввели не верный Логин или Пароль. Повторите попытку')
                return
        bot.send_message(message.chat.id, 'Поздравляю! Вы вошли в систему успешно!')


@bot.callback_query_handler(func=lambda callback: True)
def check_callback(callback):
    global reg_allow, log_allow
    if callback.data == 'positive':
        log_allow = True
        bot.send_message(callback.message.chat.id, 'Давайте залогинемся! Введите Пожалуйста ваш логин и пароль через пробел.')
    elif callback.data == 'negative':
        reg_allow = True
        bot.send_message(callback.message.chat.id, 'Введите Пожалуйста ваш логин и пароль через пробел.')


bot.infinity_polling()


