import re
import json
import asyncio
from time import strftime
from aiogram import executor, Bot, Dispatcher, types
from rich import print

with open('homeworks.json', 'r', encoding='UTF-8') as json_file:
    homeworks = json.load(json_file)

template = '''
Номер урока: {}
Урок: {}
Домашнее задание: {}
Время: {}
Ссылка: {}
'''

async def timer(time):
    while datetime.now() > time:
        asyncio.sleep(30)

bot = Bot(token='5102803513:AAEJRgR_XxoaCQYG81MwTX9zLPxMiGR9vYs')
dispatcher = Dispatcher(bot)

def return_homeworks(day):
    result = list()
    for day in homeworks.values():
        if day[0] == day:
            for lesson in day:
                if isinstance(lesson, list):
                    result.append(template.format(*lesson))
    return result


@dispatcher.message_handler(commands=['yesteday'])
async def send_yestesay(message: types.Message):
    for lesson in return_homeworks(int(strftime('%d')) - 1):
        await message.answer(lesson)


@dispatcher.message_handler(commands=['today'])
async def send_today(message: types.Message):
    for lesson in return_homeworks(int(strftime('%d'))):
        await message.answer(lesson)


@dispatcher.message_handler(commands=['/tomorrow'])
async def send_tomorrow(message:types.Message):
    for lesson in resurn_homeworks(int(strftime('%d')) + 1):
        await message.answer(lesson)


executor.start_polling(dispatcher, skip_updates=True)