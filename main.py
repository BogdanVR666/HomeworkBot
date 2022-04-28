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

bot = Bot(token='5102803513:AAEJRgR_XxoaCQYG81MwTX9zLPxMiGR9vYs')
dispatcher = Dispatcher(bot)


async def timer(time):
    while datetime.now() > time:
        asyncio.sleep(30)


def return_homeworks(date):
    result = list()
    for day in homeworks.values():
        if day[0] == date:
            for lesson in day:
                if isinstance(lesson, list):
                    result.append(template.format(*lesson))
    return result


@dispatcher.message_handler(commands=['yesteday'])
async def send_yestesay(message: types.Message):
    if lessons:=return_homeworks(int(strftime('%d')) - 1):
        for lesson in lessons:
            await message.answer(lesson)
    else:
        await message.answer('Даже я не знаю, какие вчера были уроки')


@dispatcher.message_handler(commands=['today'])
async def send_today(message: types.Message):
    if lessons:=return_homeworks(int(strftime('%d'))):
        for lesson in lessons:
            await message.answer(lesson)
    else: 
        await message.answer('Даже я не знаю, какие сегодня уроки')


@dispatcher.message_handler(commands=['now'])
async def send_now(message: types.Message):
    for day in lessons.values():
        if day[0] == int(strftime('%d')):
            for index, lesson in enumerate(day):
                if isinstance(lesson, list):
                    


@dispatcher.message_handler(commands=['tomorrow'])
async def send_tomorrow(message:types.Message):
    if lessons:=return_homeworks(int(strftime('%d')) + 1):
        for lesson in lessons:
            await message.answer(lesson)
    else:
        await message.answer('Даже я не знаю, какие завтра уроки')


executor.start_polling(dispatcher, skip_updates=True)