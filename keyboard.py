from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

yesterday_button = KeyboardButton('/yesterday')
today_button = KeyboardButton('/today')
tomorrow_button = KeyboardButton('/tomorrow')
now_button = KeyboardButton("/now")

menu = ReplyKeyboardMarkup(resize_keyboard=True).add(yesterday_button, today_button, tomorrow_button, now_button)
