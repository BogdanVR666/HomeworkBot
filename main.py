import re
import json
import asyncio
from time import strftime
from datetime import datetime
from aiogram import executor, Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from rich import print
from parser import get_lesson_by_id

template = '''
Номер урока: {0}
Урок: {1}
Время: {3}
Ссылка: <a href="{4}">перейти</a>
ID: {5}
'''

template_edited = '''
Номер урока: {0}
Урок: {1}
Время: {3}
Ссылка: <a href="{4}">перейти</a>
ID: {5}

Домашнее задание: {2}
'''

with open('homeworks.json', 'r', encoding='UTF-8') as json_file:
    homeworks = json.load(json_file)


bot = Bot(token='5102803513:AAEJRgR_XxoaCQYG81MwTX9zLPxMiGR9vYs')
dispatcher = Dispatcher(bot)

get_raw_homework_button = InlineKeyboardButton('Посмотреть запись', callback_data='get_raw_homework')
get_raw_homework_markup = InlineKeyboardMarkup().add(get_raw_homework_button)


@dispatcher.callback_query_handler(text='get_raw_homework')
async def get_raw_homework(call: types.CallbackQuery):
    lesson = get_lesson_by_id(homeworks.values(), re.search('\d{1,2}.\d{2}.\d{2}.\d{4}', call.message.text).group())
    await call.message.edit_text(template_edited.format(*lesson), parse_mode='HTML', disable_web_page_preview=True)


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
    print(message.from_user.first_name)
    await message.answer(f"Привет, {message.from_user.first_name}", reply_markup=None)


@dispatcher.message_handler(commands=['yesterday'])
async def send_yesterday(message: types.Message):
    if lessons := return_homeworks(int(strftime('%d')) - 1):
        for lesson in lessons:
            await message.answer(lesson, parse_mode='HTML', disable_web_page_preview=True, reply_markup=get_raw_homework_markup)
    else:
        await message.answer('Даже я не знаю, какие вчера были уроки')


@dispatcher.message_handler(commands=['today'])
async def send_today(message: types.Message):
    if lessons := return_homeworks(int(strftime('%d'))):
        for lesson in lessons:
            await message.answer(lesson, parse_mode='HTML', disable_web_page_preview=True, reply_markup=get_raw_homework_markup)
    else:
        await message.answer('Даже я не знаю, какие сегодня уроки')


@dispatcher.message_handler(commands=['now'])
async def send_now(message: types.Message):
    hour = int(strftime('%H'))
    minute = int(strftime('%M'))
    
    if 8 <= hour <= 16:
        if minute < 40:
            lesson_num = hour - 7
        else:
            lesson_num = hour - 6
            
    elif 0 <= hour < 8:
        lesson_num = 1
        
    elif 16 < hour:
        lesson_num = 8
        
    else:
        print(hour, minute)

    for day in homeworks.values():
        if day[0] == int(strftime('%d')):
            print()
            await message.answer(template.format(*day[lesson_num]), parse_mode='HTML', disable_web_page_preview=True, reply_markup=get_raw_homework_markup)


@dispatcher.message_handler(commands=['tomorrow'])
async def send_tomorrow(message: types.Message):
    if lessons := return_homeworks(int(strftime('%d')) + 1):
        for lesson in lessons:
            await message.answer(lesson, parse_mode='HTML', disable_web_page_preview=True, reply_markup=get_raw_homework_markup)
    else:
        await message.answer('Даже я не знаю, какие завтра уроки')


executor.start_polling(dispatcher, skip_updates=True)
