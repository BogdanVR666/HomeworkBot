import requests
import re
import json
import datetime
import calendar
from urllib3 import disable_warnings
from bs4 import BeautifulSoup
from rich import print

disable_warnings()
session = requests.Session()

csrf_class = 'csrfmiddlewaretoken'

print('getting csrf')
# getting CSRF
auth_html = session.get("https://school-5p.e-schools.info/login_", verify=False)
auth_bs = BeautifulSoup(auth_html.content, "html.parser")
csrf = auth_bs.select(f"input[name={csrf_class}]")[0]["value"]

# logging in
FormData = {
    csrf_class: csrf,
    "username": "BogdanVR666",
    "password": "BogdanVR1"
}


def search_time(string):
    regexp_time_24 = re.search(r'\d{2}:\d{2}', string)
    regexp_time_12 = re.search(r'\d{2}:\d{2} (AM|PM)', string)  # search "07:00 AM" at string
    if regexp_time_12:
        regexp_split = regexp_time_12.group().split()  # ['07:00', 'AM']
        regexp_time = regexp_split[0].split(':')  # ['07', '00']
        if regexp_split[1] == 'PM' and regexp_time[0] != '12':
            lesson_time = ':'.join((str(int(regexp_time[0]) + 12), regexp_time[1]))  # convert 12 time to 24 time
        else:
            lesson_time = regexp_split[0]
    elif regexp_time_24:
        lesson_time = regexp_time_24.group()
    else:
        lesson_time = 'урок без времени'
    return lesson_time


def search_link(string: str) -> str:
    regexp_link = re.search(r'https?://\S[^> ]+', string)
    link = regexp_link.group() if regexp_link else 'ссылок нет'
    return link


def next_monday_date(date: datetime.date) -> datetime.date:
    month_days = calendar.monthrange(date.year, date.month)[1]
    day = date.day - (date.weekday() + 1) + 7
    month = divmod(day, month_days)
    return datetime.date(date.year, date.month + month[0], month[1])


def update_site(filename: str, parsed_data: BeautifulSoup) -> None:
    if not filename.endswith('.html'):
        assert ValueError('filetype is not html')

    with open(filename, "w", encoding="UTF-8") as file:
        file.write(str(parsed_data))


def initialise_data(parse_data: BeautifulSoup) -> tuple:
    week_days = [day.text for day in parse_data.select('th.lesson')]
    days_lessons = [" ".join(str(lesson.text).split()) for lesson in parse_data.select("td.lesson > span")
                    if int(str(lesson.text).split(".")[0]) < 10]
    lessons_homeworks = [" ".join(str(homework.text).split()) for homework in parse_data.select("td.ht")]
    return week_days, days_lessons, lessons_homeworks


def create_table(days: list[str], lessons: list[str], homeworks: list[str], *, result: dict) -> None:
    score = -1

    for string in zip(lessons, homeworks):
        if string[0].startswith('1.'):
            score += 1
        try:
            result[days[score]].append((int(string[0][0]),
                                        string[0].split(maxsplit=1)[-1] if len(string[0]) > 3 else '',
                                        string[1],  # lesson
                                        search_time(string[1]),
                                        search_link(string[1])))
        except KeyError:
            result[days[score]] = [int(days[score][-2:]),
                                   (1, string[0].split(maxsplit=1)[-1] if len(string[0]) > 3 else '',
                                    string[1],
                                    search_time(string[1]),
                                    search_link(string[1]))]

    return result


response = 0
while response != 200:
    school5p = session.post("https://school-5p.e-schools.info/login_", data=FormData)
    response = school5p.status_code
    print(response)

monday = next_monday_date(datetime.datetime.now())

diary_monday = session.get(f'https://school-5p.e-schools.info/pupil/1056949/dnevnik/quarter/28553/week/{str(monday)}')
diary = session.get('https://school-5p.e-schools.info/pupil/1056949/dnevnik/quarter/28553')
print('school5p connected')

diary_bs = BeautifulSoup(diary.content, "html.parser")
diary_monday_bs = BeautifulSoup(diary_monday.content, "html.parser")
print('site parsed')

update_site('parsed.html', diary_monday_bs)
all_of_week = dict()
create_table(result=all_of_week, *initialise_data(diary_bs))
create_table(result=all_of_week, *initialise_data(diary_monday_bs))

with open('homeworks.json', 'w', encoding='UTF-8') as json_file:
    json.dump(all_of_week, json_file, ensure_ascii=False, indent=4)

print('homeworks.json rewritten')

print('Программа завершена [green]успешно[/green]. Расписание в файле [cyan]homeworks.json[/cyan]')
