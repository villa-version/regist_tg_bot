import telebot as tg


TOKEN = '6532152577:AAFqcSpzFShc2rIYrQUb6zaKxEUqCDHeLls'
bot = tg.TeleBot(TOKEN)
reg_allow = False


@bot.message_handler(commands=['start'])
def start(message):
    markup = tg.types.InlineKeyboardMarkup()
    markup.add(tg.types.InlineKeyboardButton('Да', callback_data='positive'))
    markup.add(tg.types.InlineKeyboardButton('Нет', callback_data='negative'))
    bot_text = 'Здравствуйте {name}. Вы уже зарегистрировались здесь?'.format(name=message.from_user.first_name)
    bot.send_message(message.chat.id, bot_text, reply_markup=markup)


@bot.message_handler()
def register(message):
    global reg_allow
    if reg_allow:
        try:
            login, password = message.text.split(' ')
            bot.send_message(message.chat.id, f'Ваши данные\n Login: {login}\n Password: {password}')
            reg_allow = False
        except Exception:
            bot.send_message(message.chat.id, 'Что то пошло не так! Введите еще раз!')


@bot.callback_query_handler(func=lambda callback: True)
def check_callback(callback):
    global reg_allow
    if callback.data == 'positive':
        bot.send_message(callback.message.chat.id, 'Давайте залогинемся! Введите Пожалуйста ваш логин и пароль через пробел.')
    elif callback.data == 'negative':
        reg_allow = True
        bot.send_message(callback.message.chat.id, 'Введите Пожалуйста ваш логин и пароль через пробел.')


bot.infinity_polling()

