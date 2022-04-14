import re
import asyncio
from datetime import datetime
from time import sleep
from aiogram import executor, Bot, Dispatcher, types
from parser import *

all_of_week = create_table(days=week_days, lessons=days_lessons, homeworks=lessons_homeworks)

template = '''
Урок: {lesson}
Ссылка: {link}
Время: {time}
'''

time_list = list()

for days, lessons in list(all_of_week.items()):
    for i in range(1, len(lessons)): 
        if datetime.now().day == lessons[0]:
            # lessons[i] is (num, lesson, homeworks)
            regexp_time = re.search(r'\d\d:\d\d (AM|PM)', lessons[i][2]) # search "07:00 AM" at homeworks
            if regexp_time:
                regexp_split = regexp_time.group().split() # ['07:00', 'AM']
                regexp_time = regexp_split[0].split(':') # ['07', '00']
                if regexp_split[1] == 'PM':
                    lesson_time = ':'.join((str(int(regexp_time[0]) + 12), regexp_time[1])) # convert 12 time to 24 time
                else:
                    lesson_time = regexp_split[0]
                time_list.append(lesson_time)
            else: 
                lesson_time = 'урок без времени'
            regexp_link = re.search(r'https?://[\S][^>]+', lessons[i][2]) # link search
            link = regexp_link.group() if regexp_link else None
            #print(template.format(lesson=lessons[i][1], link=link, time=lesson_time))

print('time of lessons initialised')

async def timer(time):
    while datetime.now() > time:
        asyncio.sleep(30)

bot = Bot(token='5102803513:AAEJRgR_XxoaCQYG81MwTX9zLPxMiGR9vYs')


executor.start_polling(dispatcher, skip_updates=True)