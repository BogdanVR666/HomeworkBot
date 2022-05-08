import re
import json
import asyncio
from time import strftime
from datetime import datetime
from aiogram import executor, Bot, Dispatcher, types
from rich import print
import keyboard

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


# async def timer(time):
#     while datetime.now() > time:
#         asyncio.sleep(30)


def return_homeworks(date):
    result = list()
    for day in homeworks.values():
        if day[0] == date:
            for lesson in day:
                if isinstance(lesson, list):
                    result.append(template.format(*lesson))
    return result


@dispatcher.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    await message.answer(f"Привет, {message.from_user.first_name}", reply_markup=keyboard.menu)


@dispatcher.message_handler(commands=['yesterday'])
async def send_yesterday(message: types.Message):
    if lessons := return_homeworks(int(strftime('%d')) - 1):
        for lesson in lessons:
            await message.answer(lesson)
    else:
        await message.answer('Даже я не знаю, какие вчера были уроки')


@dispatcher.message_handler(commands=['today'])
async def send_today(message: types.Message):
    if lessons := return_homeworks(int(strftime('%d'))):
        for lesson in lessons:
            await message.answer(lesson)
    else:
        await message.answer('Даже я не знаю, какие сегодня уроки')


@dispatcher.message_handler(commands=['now'])
async def send_now(message: types.Message):
    date = int(strftime('%H'))
    if 8 <= date <= 16:
        lesson_num = date - 7
    elif 0 <= date < 8:
        lesson_num = 1
    elif 16 < date:
        lesson_num = 8
    else:
        print(date)

    for day in homeworks.values():
        if day[0] == int(strftime('%d')):
            await message.answer(template.format(*day[lesson_num]))


@dispatcher.message_handler(commands=['tomorrow'])
async def send_tomorrow(message: types.Message):
    if lessons := return_homeworks(int(strftime('%d')) + 1):
        for lesson in lessons:
            await message.answer(lesson)
    else:
        await message.answer('Даже я не знаю, какие завтра уроки')


executor.start_polling(dispatcher, skip_updates=True)
