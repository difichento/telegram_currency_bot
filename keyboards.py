from telebot import types

menu_keyboard = types.ReplyKeyboardMarkup(True)
menu_keyboard.row("Курс валют к рублю")
menu_keyboard.row("Перевести валюту")
menu_keyboard.row("Рассылка")

currency_keyboard = types.ReplyKeyboardMarkup(True)
currency_keyboard.row("RUB", "USD", "EUR")
currency_keyboard.row("UAH", "BYN", "PLN")

quantity_keyboard = types.ReplyKeyboardMarkup(True)
quantity_keyboard.row("1", "50", "100", "500", "1000")

mailing_keyboard = types.ReplyKeyboardMarkup(True)
mailing_keyboard.row("Подписаться", "Отписаться")
mailing_keyboard.row("Выбрать валюту")
mailing_keyboard.row("Назад")
