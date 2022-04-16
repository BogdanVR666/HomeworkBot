import requests
from urllib3 import disable_warnings
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
        for i, j in zip(lessons, homeworks):
            if "1." in i and "11." not in i:
                file.write(f"\n{days[x]}\n")
                x += 1
            file.write(f"{i} {j}\n") if len(i) > 3 else None


def create_table(days: list, lessons: list, homeworks: list):
    result = dict()
    score = -1

    for i in zip(lessons, homeworks):
        score += 1 if "1." in i[0] and "11." not in i[0] else 0
        try:
            result[days[score].split()[0]].append((int(i[0][0]),
                                                   i[0].split(maxsplit=1)[-1] if len(i[0]) > 3 else '',
                                                   i[1]))
        except KeyError:
            result[days[score].split()[0]] = [int(days[score][-2:]),
                                              (int(i[0][0]),
                                               i[0].split(maxsplit=1)[-1] if len(i[0]) > 3 else '', i[1])]

    return result

responce = 0
while responce != 200:
    school5p = session.post("https://school-5p.e-schools.info/login_", data=FormData)
    responce = school5p.status_code

shodennik = session.get('https://school-5p.e-schools.info/pupil/1056949/dnevnik/quarter/28553')
print('school5p connected')

pupil_bs = BeautifulSoup(shodennik.content, "html.parser")
print('site parsed')

week_days = [i.text for i in pupil_bs.select('th.lesson')]
days_lessons = [" ".join(str(i.text).split()) for i in pupil_bs.select("td.lesson > span")]
lessons_homeworks = [" ".join(str(i.text).split()) for i in pupil_bs.select("td.ht")]
print('school data initialised')

if __name__ == '__main__':
    update_site('parsed.html')
    write_table('homeworks.txt', days=week_days, lessons=days_lessons, homeworks=lessons_homeworks)
    all_of_week = create_table(days=week_days, lessons=days_lessons, homeworks=lessons_homeworks)
    rint('Программа завершена [green]успешно[/green]. Расписание в файле [cyan]homeworks.txt[/cyan]')
