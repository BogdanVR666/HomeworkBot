import requests
from urllib3 import disable_warnings
import json
from bs4 import BeautifulSoup
from rich import print as rint

disable_warnings()
session = requests.Session()

csrfclass = 'csrfmiddlewaretoken'

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


def update_site(filename):
    assert filename.endswith('.html'), "type is not html"

    with open(filename, "w", encoding="UTF-8") as file:
        file.write(str(pupil_bs))


def write_table(filename, days, lessons, homeworks):
    with open(filename, "w", encoding="UTF-8") as file:
        x = 0
        for lesson, homework in zip(lessons, homeworks):
            if lesson.startswith('1.'):
                file.write(f"\n{days[x]}\n")
                x += 1
            if len(lesson) > 3:
                file.write(f"{lesson} {homework}\n")


def create_table(days: list, lessons: list, homeworks: list) -> dict:
    result = dict()
    score = -1

    for line in zip(lessons, homeworks):
        if line[0].startswith('1.'):
            score += 1
        try:
            result[days[score].split()[0]].append((int(line[0][0]),
                                                   line[0].split(maxsplit=1)[-1] if len(line[0]) > 3 else '',
                                                   line[1]))
        except KeyError:
            result[days[score].split()[0]] = [int(days[score][-2:]),
                                              (int(line[0][0]),
                                               line[0].split(maxsplit=1)[-1] if len(line[0]) > 3 else '', line[1])]

    return result


server_answer = 0
while server_answer != 200:
    school5p = session.post("https://school-5p.e-schools.info/login_", data=FormData)
    server_answer = school5p.status_code

shodennik = session.get('https://school-5p.e-schools.info/pupil/1056949/dnevnik/quarter/28553')
print('school5p connected')

pupil_bs = BeautifulSoup(shodennik.content, "html.parser")
print('site parsed')

week_days = [day.text for day in pupil_bs.select('th.lesson')]
days_lessons = [" ".join(str(lesson_line.text).split()) for lesson_line in pupil_bs.select("td.lesson > span")]
lessons_homeworks = [" ".join(str(i.text).split()) for i in pupil_bs.select("td.ht")]
print('school data initialised')

if __name__ == '__main__':
    update_site('parsed.html')
    print('parsed.html is rewrited')
    write_table('homeworks.txt', days=week_days, lessons=days_lessons, homeworks=lessons_homeworks)
    print('homeworks.txt rewrited')
    all_of_week = create_table(days=week_days, lessons=days_lessons, homeworks=lessons_homeworks)
    with open('homeworks.json', 'w', encoding='UTF-8') as json_file:
        json.dump(all_of_week, json_file, ensure_ascii=False, indent=4)
    print('homeworks.json rewrited')
    rint('Программа завершена [green]успешно[/green]. Расписание в файле [cyan]homeworks.txt[/cyan]')
