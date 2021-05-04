from pycbrf import ExchangeRates

from globals import bot
from keyboards import currency_keyboard, menu_keyboard, quantity_keyboard


class Currency:
    """
    Библиотека pycbrf выдает стоимость валюты в рублях,
    соответственно валюты RUB там нет, поэтому создаем класс-затычку
    """

    def __init__(self):
        self.name = "Российский рубль"
        self.rate = 1
        self.code = "RUB"


RUBcurrency = Currency()

currency1 = None
currency1_quantity = None
currency2 = None
rates = None


def converter_for_main_menu(message):
    bot.send_message(message.chat.id, "Выберите из какой валюты перевести", reply_markup=currency_keyboard)
    bot.register_next_step_handler(message, converter_step1)


def converter_step1(message):
    """
    Проверяет выбранную валюту на корректность и сохраняет в currency1
    Переходит к шагу converter_step2
    """
    global currency1, rates
    rates = ExchangeRates()
    if message.text == "RUB":
        currency1 = RUBcurrency
    else:
        currency1 = rates[message.text]
    if currency1 is None:
        bot.send_message(message.chat.id, "я не знаю такую валюту", reply_markup=menu_keyboard)
        return
    else:
        bot.send_message(message.chat.id, "Выберите в какую валюту перевести", reply_markup=currency_keyboard)
        bot.register_next_step_handler(message, converter_step2)


def converter_step2(message):
    """
    Проверяет выбранную валюту на корректность и сохраняет в currency2
    Переходит к шагу converter_step3
    """
    global currency2
    if message.text == "RUB":
        currency2 = RUBcurrency
    else:
        currency2 = rates[message.text]

    if currency2 is None:
        bot.send_message(message.chat.id, "я не знаю такую валюту", reply_markup=menu_keyboard)
        return
    else:
        bot.send_message(message.chat.id, f"Выберите сколько {currency1.name} перевести в {currency2.name}",
                         reply_markup=quantity_keyboard)
        bot.register_next_step_handler(message, converter_step3)


def converter_step3(message):
    """
    Сохраняет выбранное количество валюты в currency1_quantity
    """
    global currency1_quantity
    try:
        currency1_quantity = float(message.text)
    except ValueError:
        bot.send_message(message.chat.id, "что-то пошло не так", reply_markup=menu_keyboard)
        return
    if currency1_quantity < 0:
        bot.send_message(message.chat.id, "как ты собрался отрицательные деньги переводить",
                         reply_markup=menu_keyboard)
    else:
        convert_currency(message)


def convert_currency(message):
    """
    Отправляет результат конвертации
    """
    res = currency1_quantity * float(currency1.rate) / float(currency2.rate)
    bot.send_message(message.chat.id, f"{currency1_quantity} {currency1.code} = {round(res, 3)} {currency2.code}",
                     reply_markup=menu_keyboard)
