import requests
from urllib3 import disable_warnings
from bs4 import BeautifulSoup
from rich import print

disable_warnings()
session = requests.Session()

# getting CSRF
auth_html = session.get("https://school-5p.e-schools.info/login_", verify=False)
auth_bs = BeautifulSoup(auth_html.content, "html.parser")
csrf = auth_bs.select("input[name=csrfmiddlewaretoken]")[0]["value"]

# logging in
FormData = {
    "csrfmiddlewaretoken": csrf,
    "username": "BogdanVR666",
    "password": "BogdanVR1"
}

domen = "https://school-5p.e-schools.info"

pupil = None

while not pupil:
    answer = session.post(domen + "/login_", data=FormData)
    answer_bs = BeautifulSoup(answer.content, "html.parser")
    pupils = answer_bs.select("a.user_type_1")
    pupil = domen + pupils[0]["href"] + "/dnevnik/quarter/28553" if pupils else None

pupil_bs = BeautifulSoup(session.get(pupil).content, "html.parser")

with open("parsed.html", "w", encoding="UTF-8") as file:
    file.write(str(pupil_bs))

lessons = [" ".join(str(i.text).split()) for i in pupil_bs.select("td.lesson > span")]
homeworks = [" ".join(str(i.text).split()) for i in pupil_bs.select("td.ht")]
days = [i.text for i in pupil_bs.select('th.lesson')]

with open("homeworks.txt", "w", encoding="UTF-8") as result:
    x = 0
    for i, j in zip(lessons, homeworks):
        if "1." in i and "11." not in i:
            result.write(f"\n{days[x]}\n")
            x += 1
        result.write(f"{i} {j}\n") if len(i) > 3 else None

print('[green]Программа завершена успешно. Расписание в файле homeworks.txt[/green]')
