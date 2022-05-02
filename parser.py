import requests
import re
import json
from time import strftime
from urllib3 import disable_warnings
from bs4 import BeautifulSoup
from rich import print as rint

disable_warnings()
session = requests.Session()

csrfclass = 'csrfmiddlewaretoken'

print('getting csrf')
# getting CSRF
auth_html = session.get("https://school-5p.e-schools.info/login_", verify=False)
auth_bs = BeautifulSoup(auth_html.content, "html.parser")
csrf = auth_bs.select(f"input[name={csrfclass}]")[0]["value"]

# logging in
FormData = {
    csrfclass: csrf,
    "username": "BogdanVR666",
    "password": "BogdanVR1"
}


def search_time(string):
    regexp_time_24 = re.search(r'[0-9]{2}:[0-9]{2}', string)
    regexp_time_12 = re.search(r'[0-9]{2}:[0-9]{2} (AM|PM)', string) # search "07:00 AM" at string
    if regexp_time_12:
        regexp_split = regexp_time_12.group().split() # ['07:00', 'AM']
        regexp_time = regexp_split[0].split(':') # ['07', '00']
        if regexp_split[1] == 'PM' and regexp_time[0] != '12':
            lesson_time = ':'.join((str(int(regexp_time[0]) + 12), regexp_time[1])) # convert 12 time to 24 time
        else:
            lesson_time = regexp_split[0]
    elif regexp_time_24:
        lesson_time = regexp_time.group()
    else: 
        lesson_time = 'урок без времени'
    return lesson_time


def search_link(string):
    regexp_link = re.search(r'https?://[\S][^>]+', string)
    link = regexp_link.group() if regexp_link else 'ссылок нет'
    return link


def update_site(filename):
    if not filename.endswith('.html'):
        assert ValueError('filetype is not html')

    with open(filename, "w", encoding="UTF-8") as file:
        file.write(str(pupil_bs))


def write_table(filename, days, lessons, homeworks):
    with open(filename, "w", encoding="UTF-8") as file:
        x = 0
        for i, j in zip(lessons, homeworks):
            if "1." in i and "11." not in i:
                file.write(f"\n{days[x]}\n")
                x += 1
            file.write(f"{i} {j}\n") if len(i) > 3 else None


def create_table(days: list, lessons: list, homeworks: list):
    result = dict()
    score = -1

    for string in zip(lessons, homeworks):
        if string[0].startswith('1.'):
            score += 1
        try:
            result[days[score].split()[0]].append((int(string[0][0]),
                                                   string[0].split(maxsplit=1)[-1] if len(string[0]) > 3 else '', # lesson
                                                   string[1],
                                                   search_time(string[1]),
                                                   search_link(string[1])))
        except KeyError:
            result[days[score].split()[0]] = [int(days[score][-2:]),
                                              (1, string[0].split(maxsplit=1)[-1] if len(string[0]) > 3 else '', 
                                              string[1],
                                              search_time(string[1]),
                                              search_link(string[1]))]

    return result

responce = 0
while responce != 200:
    school5p = session.post("https://school-5p.e-schools.info/login_", data=FormData)
    responce = school5p.status_code
    print(responce)

shodennik = session.get(strftime('https://school-5p.e-schools.info/pupil/1056949/dnevnik/quarter/28553/week/%Y-%m-%d'))
print('school5p connected')

pupil_bs = BeautifulSoup(shodennik.content, "html.parser")
print('site parsed')

week_days = [i.text for i in pupil_bs.select('th.lesson')]
days_lessons = [" ".join(str(i.text).split()) for i in pupil_bs.select("td.lesson > span")]
lessons_homeworks = [" ".join(str(i.text).split()) for i in pupil_bs.select("td.ht")]
print('school data initialised')

update_site('parsed.html')
write_table('homeworks.txt', days=week_days, lessons=days_lessons, homeworks=lessons_homeworks)
all_of_week = create_table(days=week_days, lessons=days_lessons, homeworks=lessons_homeworks)
with open('homeworks.json', 'w', encoding='UTF-8') as json_file:
    json.dump(all_of_week, json_file, ensure_ascii=False, indent=4)
print('homeworks.json rewrited')


rint('Программа завершена [green]успешно[/green]. Расписание в файле [cyan]homeworks.txt[/cyan]')
