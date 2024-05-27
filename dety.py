import telebot
from telebot import types
import random

def read_lines_to_fullList():
    students = []
    with open('fullList.txt', 'r', encoding='utf-8') as file:
        for line in file:
            students.append(line.strip())
        return students

def read_lines_to_currentList():
    students = []
    with open('currentList.txt', 'r', encoding='utf-8') as file:
        for line in file:
            students.append(line.strip())
        return students
    
def write_names_to_currentList(names_list):
    with open('currentList.txt', 'w', encoding='utf-8') as file:
        for name in names_list:
            file.write(name + '\n')

API_TOKEN = '7400403502:AAEYpOgni0Str4OvYlWtjqMvRPzS2LCmp9U'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    menu_button = types.KeyboardButton('Новый раб😘')
    markup.add(menu_button)

    bot.send_message(message.chat.id, "Идите работайте, ЛЕНТЯИ!!!", reply_markup=markup)

@bot.message_handler(regexp="Новый раб😘")
def send_random_name(message):
    
    if len(read_lines_to_currentList()) == 0:
        write_names_to_currentList(read_lines_to_fullList())
        bot.send_message(message.chat.id, "🔞 Рабы перезаряжены 🔞")
    
    names = read_lines_to_currentList()
    name = names[random.randint(0, (len(names) - 1))]
    
    markup = types.InlineKeyboardMarkup()
    skip_button = types.InlineKeyboardButton('Сегодня отдыхает😇', callback_data='skip')
    use_button = types.InlineKeyboardButton('Этот пашет👍', callback_data=f'use_{name}')
    markup.add(skip_button, use_button)
    
    bot.send_message(message.chat.id, '{} - пойдет работать?'.format(name), reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('use_') or call.data == 'skip')
def callback_inline(call):
    if call.data == 'skip':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        send_random_name(call.message)

    elif call.data.startswith('use_'):
        name_to_remove = call.data.split('_')[1]

        names = read_lines_to_currentList()
        names.remove(name_to_remove)
        write_names_to_currentList(names)

        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, f"{name_to_remove} отправлен на каторги😊")

        if len(read_lines_to_currentList()) == 0:
            write_names_to_currentList(read_lines_to_fullList())
            bot.send_message(call.message.chat.id, "🔞 Рабы перезаряжены 🔞")

bot.polling(none_stop=True)