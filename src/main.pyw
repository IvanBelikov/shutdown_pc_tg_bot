import telebot
from telebot import types
import os
import json

# Read bot token from JSON file
bot_token = json.load(open('./utils/bot_token.json'))
# Initialize bot
bot = telebot.TeleBot(bot_token['token'])


def action(message):
    keyboard = types.InlineKeyboardMarkup()
    shutdown_btn = types.InlineKeyboardButton(text='Выключить ПК', callback_data='shutdown')
    reboot_btn = types.InlineKeyboardButton(text='Перезагрузить ПК', callback_data='reboot')
    question = 'Выберите действие'
    keyboard.add(shutdown_btn)
    keyboard.add(reboot_btn)
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "/start" and message.from_user.id == 409451600:
        action(message)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "shutdown":
        bot.send_message(call.message.chat.id, 'Выключаю')
        print('poweroff')
        os.system('shutdown -s /t 0 /f')

    elif call.data == "reboot":
        bot.send_message(call.message.chat.id, 'Перезагружаю')
        os.system('shutdown -r /t 0 /f')

bot.polling(none_stop=True, interval=0)
