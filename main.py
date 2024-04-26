import telebot
import sqlite3
import threading
from termcolor import colored
import speech_recognition


bot = telebot.TeleBot('7176018058:AAGfuFcUxilC8zVh49bA2LIZcxmsgEvfvIs')
conn = sqlite3.connect('sqlite_db.sqlite', check_same_thread=False)
cursor = conn.cursor()
lock = threading.Lock()


def get_mes(message, caption=None):
    with lock:
        sql_query = "INSERT or REPLACE INTO users_id (name, last_name, tag, id) VALUES (?, ?, ?, ?)"
        cursor.execute(sql_query, (message.from_user.first_name, message.from_user.last_name,
                                   message.from_user.username, message.from_user.id))
        conn.commit()

    if caption is None:
        text = message.text
    else:
        text = caption
    if message.from_user.last_name is None:
        return f'{colored(message.from_user.first_name, "green")}: {text}'
    return (f'{colored(message.from_user.first_name, "green")} {colored(message.from_user.last_name, "green")}:'
            f' {text}')


@bot.message_handler(commands=['start'])
def facts(message):
    print(get_mes(message))
    bot.reply_to(message, f"Привет!🖐\nЯ чат-бот технической поддержки для куратора второго пилота!")


print('ЗАПУЩЕНО!')
bot.polling()