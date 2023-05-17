"""1)импортируем класс бота и специальный тип данных для того, чтобы писать 
   анотации типов в функциях бота.
   2)импортируем класс диспетчер для реакции бота(он улавливает события в чате 
   или события отправки пользователем сообщения боту).
   3)импортируем экзекьютер для запуска бота онлайн. 

   методы работы с ботом:
   1)LongPolling - бот запускается на локальной машине и обращается к серверу Telegaram(для тестов)
   2)Webhook - бот развёртывается на сервере и сервер telegram обращается к боту(для работы)
"""
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

import os # нужен, чтобы прочитать токен из переменной среды окружения
import json
import rent_calc as rc
import re

# Токен от renc_calc
# TOKEN = '5438220805:AAHy4k6LuEMYfK4pgU54JbrGRX7sRYUy_Qk'

bot = Bot(token=os.getenv('TOKEN')) # Инициализируем бота.
# bot = Bot(token=TOKEN)
dp = Dispatcher(bot) # Инициализируем диспетчер куда передаём экземпляр бота.


async def on_startup(_):
    print('Bot is online')


@dp.message_handler(commands=['start'])
async def command_start(message : types.Message):
    cleanFile(message.from_id)
    await bot.send_message(message.from_user.id, 'Введите дату ЗАЕЗДА в формате дд.мм')

@dp.message_handler(commands=['cancel'])
async def command_start(message : types.Message):
    cleanFile(message.from_id)


@dp.message_handler()
async def for_user(message : types.Message):
    result = ''
    f = open('msgs/' + repr(message.from_id) + '.txt', 'r')
    params = json.loads(f.readline()) # преоброзует json в словарь
    step = int(params['step'])
    f.close()
    if step == 1:
        result = rc.guest_arrival(message.text)
        if result == 'ok':
            f = open('msgs/' + repr(message.from_id) + '.txt', 'w')
            f.write('{"step": 2, "arrival":  "'
                    + repr(message.text)
                    + '"}')
            
            result = f"ЗАЕЗД - {message.text}.2023г.,\n введите дату ВЫЕЗДА в формате дд.мм"
            f.close()

    elif step == 2:
        result = rc.guest_departure(message.text)
        if result == 'ok':
            f = open('msgs/'+ repr(message.from_id) + '.txt', 'w') 
            f.write('{"step": 3, "arrival": ' 
                    +  repr(params["arrival"])
                    + ', "departure": "' 
                    + repr(message.text) 
                    + '"}')
            
            result = f"ВЫЕЗД - {message.text}.2023г.,\n введите номер апартаментов от 1 до 8"
            f.close()

    elif step == 3:
        result = rc.appart_number(message.text)
        if result == "ok":
            f = open('msgs/' + repr(message.from_id) + '.txt', 'w')
            f.write('{"step": 4, "arrival": '
                    + repr(params["arrival"])
                    + ', "departure": '
                    + repr(params["departure"])
                    + ', "apartment": "'
                    + repr(message.text)
                    + '"}')
            
            result = f"Апартаменты № {message.text},\n Введите размер скидки в %"
            f.close()

    elif step == 4:
        result = rc.discount(message.text)
        if result == "ok":
            f = open('msgs/' + repr(message.from_id) + '.txt', 'w')
            f.write('{"step": 5, "arrival": '
                    + repr(params["arrival"])
                    + ', "departure": '
                    + repr(params["departure"])
                    + ', "apartment": '
                    + repr(params["apartment"])
                    + ', "discount": "'
                    + repr(message.text)
                    + '"}')
            result = 'чтобы посчитать введите абсолютно любой символ'
            f.close()

    else:
        str1 = params['arrival']
        str2 = params['departure']
        str3 = params['apartment']
        str4 = params['discount']
        arriv = re.findall(r"\d+", str1)
        dep = re.findall(r"\d+", str2)
        apart = re.findall(r"\d", str3)[0]
        discount = int(re.findall(r"\d+", str4)[0])
        
        result = rc.calculate(arriv, dep, apart, discount)
        cleanFile(message.from_id)
 
    await message.answer(result)

def cleanFile(name):
    with open('msgs/' + repr(name) + '.txt', 'w') as f:
        f.write('{"step": 1}')



executor.start_polling(dp, skip_updates=True, on_startup=on_startup) # Команда запуска бота.
