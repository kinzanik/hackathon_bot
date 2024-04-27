import torch
import torch.nn as nn
import logging
import telebot
import sqlite3
import threading
from termcolor import colored
import speech_recognition
from stt import *
from model_ai import *


bot = telebot.TeleBot('7176018058:AAGfuFcUxilC8zVh49bA2LIZcxmsgEvfvIs')
conn = sqlite3.connect('sqlite_db.sqlite', check_same_thread=False)
cursor = conn.cursor()
lock = threading.Lock()

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def record_and_recognize_audio(*args: tuple, do='default'):
    pass


def get_mes(message, caption=None):
    with lock:
        sql_query = "INSERT or REPLACE INTO users_id (name, last_name, tag, id) VALUES (?, ?, ?, ?)"
        cursor.execute(sql_query, (message.from_user.first_name, message.from_user.last_name,
                                   message.from_user.username, message.from_user.id))
        conn.commit()

    if message.from_user.id == 2071811935:
        bot.reply_to(message, 'иди нахуй')
    if caption is None:
        text = message.text
    else:
        text = caption
    if message.from_user.last_name is None:
        return f'{colored(message.from_user.first_name, "green")}: {text}'
    return (f'{colored(message.from_user.first_name, "green")} {colored(message.from_user.last_name, "green")}:'
            f' {text}')


# Модель для анализа вопросов пользователей
class QuestionAnalyzer(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(QuestionAnalyzer, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        out = self.fc1(x)
        out = self.relu(out)
        out = self.fc2(out)
        return out


def get_answer(question):
    return knowledge_base.get(question,
                              "Извините, я не могу ответить на этот вопрос. Хотите связаться с живым куратором?")


def call_curator():
    return "Подождите немного, с вами свяжется живой куратор."


@bot.message_handler(content_types=['voice'])
def voice_handler(message):
    voice_duration = message.voice.duration
    minutes = voice_duration // 60
    seconds = voice_duration % 60
    print(get_mes(message, caption=f'<Voice message {minutes:02}:{seconds:02}>'))
    file = bot.get_file(message.voice.file_id)
    bytes = bot.download_file(file.file_path)
    with open('voice.ogg', 'wb') as f:
        f.write(bytes)
    text = speech_to_text()
    if text is None:
        bot.send_message(message.chat.id, 'Я не понял вопрос, повторите еще раз')
    else:
        answer_text = predict_answer_with_text(text)
        print("Предсказанный ответ:", answer_text)
        bot.send_message(message.chat.id, answer_text)




@bot.message_handler(commands=['start'])
def start(message):
    print(get_mes(message))
    bot.reply_to(message, f"Привет, {message.from_user.first_name}!🖐\n"
                          f"Я чат-бот технической поддержки для куратора второго пилота!\n"
                          f"Напиши /help для получения информации")


@bot.message_handler(commands=['help'])
def help(message):
    print(get_mes(message))
    help_message = "Список доступных команд:\n"
    help_message += "/start - начать диалог с ботом\n"
    help_message += "/help - получить справку о доступных командах\n"
    bot.send_message(message.chat.id, help_message)


@bot.message_handler(commands=['call_curator'])
def call_curator(message):
    print(get_mes(message))
    bot.reply_to(message, call_curator())


@bot.message_handler(func=lambda message: True)
def answer_question(message):
    print(get_mes(message))
    question = message.text
    answer_text = predict_answer_with_text(question)
    print("Предсказанный ответ:", answer_text)
    bot.reply_to(message, answer_text)


print('Запущено')
bot.polling()