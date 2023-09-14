# -*- coding: utf-8 -*-

#import pyowm
import config
import datetime
import telebot
import time
import paho.mqtt.client as mqtt
#import xlrd
from telebot import types

#функции для коннекта к mqtt
def on_message(client, obj, msg):
    print((str(msg.payload)[2:7]))
    pogoda = (str(msg.payload)[2:7])

def on_publish(client, obj, mid):
    print()

def keyboard(where_call):
    kb = types.InlineKeyboardMarkup()
    if where_call == 'start':
        kb_1 = types.InlineKeyboardButton(text='1_1_inline', callback_data='1_1_inline')
        kb.add(kb_1)
        return kb
    elif where_call == 'subcategory':
        kb_2 = types.InlineKeyboardButton(text='2_1_inline', callback_data='2_1_inline')
        kb.add(kb_2)
        return kb
    elif where_call == 'product':
        kb_3 = types.InlineKeyboardButton(text='3_1_inline', callback_data='3_1_inline')
        kb.add(kb_3)
        return kb


#from pyowm import OWM
#owm = pyowm.OWM('1884e6b6d5605fee686cf449ac8b1e54', language= 'RU')
bot = telebot.TeleBot(config.token)


#Месяц
today = datetime.datetime.today()
mount = ['Января', 'Февраля', 'Марта', 'Апреля', 'Апреля', 'Июня', 'Июля', 'Августа', 'Сентября', 'Октября', 'Ноября', 'Декабря']
mounth_real = int(today.strftime("%m"))

#день и месяц текстом
day = today.strftime("%A")
if day == 'Monday':
    day = 'понедельник'
elif day == 'Tuesday':
    day = "вторник"
elif day == 'Wednesday':
    day = "среда"
elif day == 'Thursday':
    day = "четверг"
elif day == 'Friday':
    day = "пятница"
elif day == 'Saturday':
    day = "суббота"
elif day == 'Sunday':
    day = "Воскресенье"


#observation = owm.weather_at_place('Москва')
#w = observation.get_weather()
#temp = w.get_temperature('celsius')['temp']


text1 = ('Сегодня ' + day + ',  ' + today.strftime("%d") + ' ' + mount[mounth_real % 12] + ' ' + today.strftime(
    "%Y") + ' г.')
#text2 = ('Погода в Москве хорошая, ' + w.get_detailed_status() + ' ' + str(round(temp)) + ' °C')
text2 = ('Погода в Москве хорошая, сколько то там градусов °C')


@bot.message_handler(content_types=["text"])
def message(message):
    users_id = message.chat.id
    users_name = message.chat.first_name
    timers = datetime.datetime.today().strftime("%d.%m.%Y %H:%M:%S")
    doc = open('stat/stat.txt', 'a', encoding='utf-8')
    doc.write(f'{users_id} : {users_name} : {timers} - start\n')
    doc.close

    bot.send_message(message.chat.id, f"Привет {users_name}! Это бот БДАРМ")
    time.sleep(0)
    bot.send_message(message.chat.id, text1)
    time.sleep(0)
    bot.send_message(message.chat.id, text2)
    time.sleep(0)

    mqttc = mqtt.Client()
    mqttc.on_message = on_message
    mqttc.on_publish = on_publish
    topic_temp = 'esp32/bme280/temperature'
    mqttc.username_pw_set('u_HK44NE', 'MHOVlxC4')
    mqttc.connect("m5.wqtt.ru", 7672)
    temp = mqttc.subscribe(topic_temp, 0)

    markup = telebot.types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton('Да', callback_data='start')
    markup.row(button1)
    bot.send_message(message.from_user.id,f"Поехали?", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == 'start':
        markup = telebot.types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton('☔  Узнать температуру в отделе  ☔', callback_data='one')
        button2 = types.InlineKeyboardButton('🧑‍💻 Сгенерить СЕТУНЬ 🧑‍💻', callback_data='two')
        button3 = types.InlineKeyboardButton('🧑‍💻 Сгенерить рабочие планы 🧑‍💻', callback_data='three')
        markup.row(button1)
        markup.row(button2)
        markup.row(button3)
        bot.send_message(call.message.chat.id, 'Что будем делать?', reply_markup=markup)


    elif call.data == 'one':
        bot.send_message(call.message.chat.id, '==================')
        bot.send_message(call.message.chat.id, 'Температура в офисе нормальная')
        markup = telebot.types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton('Назад', callback_data='start')
        markup.row(button1)
        bot.send_message(call.message.chat.id, '==================', reply_markup=markup)
    elif call.data == 'two':
        bot.send_message(call.message.chat.id, '==================')
        bot.send_message(call.message.chat.id, 'Функция в разработке')
        markup = telebot.types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton('Назад', callback_data='start')
        markup.row(button1)
        bot.send_message(call.message.chat.id, '==================', reply_markup=markup)
    elif call.data == 'three':
        bot.send_message(call.message.chat.id, '==================')
        bot.send_message(call.message.chat.id, 'Функция в разработке')
        markup = telebot.types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton('Назад', callback_data='start')
        markup.row(button1)
        bot.send_message(call.message.chat.id, '==================', reply_markup=markup)


    #bot.reply_to(message, "Что будем длать?!", reply_markup=keyboard('start'))

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == '1_1_inline':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='подкатегория', reply_markup=keyboard('subcategory'))

    elif call.data == '2_1_inline':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='товар', reply_markup=keyboard('product'))
    elif call.data == '3_1_inline':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Описание товара')
        bot.send_photo(call.message.chat.id,
                       'https://cs13.pikabu.ru/images/big_size_comm/2020-06_3/159194100716237333.jpg')


bot.polling(none_stop=True, interval=0)
