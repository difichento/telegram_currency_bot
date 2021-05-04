import pandas as pd
import requests
import re
from bs4 import BeautifulSoup

from globals import bot


def send_courses(message):
    """
    Парсит сайт alta.ru и получает таблицу валют и их стоимостей
    """
    req = requests.get("https://www.alta.ru/currency/")
    soup = BeautifulSoup(req.content, 'html.parser')
    rows = soup.findAll("tr")
    for i in range(len(rows)):
        rows[i].prettify()
    rows = rows[7:34]
    rows = list(map(lambda x: BeautifulSoup(x.prettify(), 'html.parser'), rows))
    data = {"Currency": [], "Quantity": [], "Cost in RUB": []}
    for row in rows:
        currency = row.findAll("span", {"class": "gray"})[0].text
        quantity = row.findAll("span", {"class": "gray"})[1].text
        cost = row.find("td", {"style": None, "class": None}).text

        currency = re.sub(r'\s+', '', currency)
        quantity = re.sub(r'\s+', '', quantity)
        quantity = quantity[3:quantity.find(")")]
        cost = re.sub(r'\s+', '', cost)

        data["Currency"].append(currency)
        data["Quantity"].append(quantity)
        data["Cost in RUB"].append(cost)
    bot.send_message(message.chat.id, "```\n" + pd.DataFrame(data).to_string() + "\n```", parse_mode="Markdown")
