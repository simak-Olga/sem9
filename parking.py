import telebot
from random import *
import json
from telebot import types

parking = []

def save():
    with open("parking.json","w",encoding="utf-8") as fh:
        fh.write(json.dumps(parking,ensure_ascii=False))
    print("Парковка готова и сохранена в файле parking.json")

def load():
    global parking
    with open("parking.json","r",encoding="utf-8") as fh:
        parking=json.load(fh)
    print("Парковочные места под машины загружены")   

API_TOKEN=('5469125157:AAErjBPsJmi9I0wL0SuwRlbqnDVc_gxKta0')
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def start_message(message):
    try:
        load()
        bot.send_message(message.chat.id,"Приветствую, парковочные места под машины загружены!")
        bot.send_photo(message.chat.id, "https://img.freepik.com/premium-photo/some-cars-underground-parking_214122-80.jpgw=1380")
       
    except:
        parking.append("101")
        parking.append("132")
        parking.append("148")
        parking.append("155")
        parking.append("163") 
        bot.send_message(message.chat.id,"Парковочные места под машины загружены по умолчанию!")

@bot.message_handler(commands=['all'])
def show_all(message):
    bot.send_message(message.chat.id,"Вот список парковочных мест")
    bot.send_message(message.chat.id, ", ".join(parking))

@bot.message_handler(content_types='text')
def message_reply(message):
    if message.text=="Кнопка":
      markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
      item1=types.Keyboardbutton("Кнопка2")
      bot.send_message(message.chat.id,'Выберите, что Вам нужно', reply_markup=markup)
    elif message.text =="Кнопка 2":
      bot.send_message(message.chat.id,'Cпасибо, что зашли!')

bot.polling()
