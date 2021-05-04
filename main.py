import schedule
from time import sleep
from threading import Thread

from converter import converter_for_main_menu
from courses import send_courses
from globals import bot, users_database
from keyboards import currency_keyboard, mailing_keyboard, menu_keyboard
from mailing import mailing_for_main_menu, do_mailing


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id,
                     "Привет! Я  помогу тебе узнать курс валют. Для помощи набери /help", reply_markup=menu_keyboard)


@bot.message_handler(commands=["help"])
def help(message):
    bot.send_message(message.chat.id, """РОССИЯ РОССИЯ РОССИЯ РОССИЯ РОССИЯ 

Для навигации используйте кнопки на клавиатуре 

Если вы подпишитесь на рассылку я каждый день в 8:21 МСК буду присылать \
изменение выбранной валюты в сравнении с предыдущим днём""",
                     reply_markup=menu_keyboard)


@bot.message_handler(commands=["force"])
def force_mailing(message):
    do_mailing()


@bot.message_handler(content_types=["text"])
def menu(message):
    """
    Обрабатывает все сообщения, кроме комманд, которые прописаны выше.
    Все message которые передаются в функции нужны в основном для того чтобы сохранить chat_id
    """
    print(message.chat.id, message.text)

    command_list = {"курс валют к рублю": send_courses,
                    "перевести валюту": converter_for_main_menu,
                    "рассылка": mailing_for_main_menu}

    if message.text.lower() in command_list.keys():
        command_list[message.text.lower()](message)
    else:
        bot.send_message(message.chat.id, "не понял", reply_markup=menu_keyboard)
        bot.register_next_step_handler(message, menu)


def time_checker():
    """
    Проверка времени
    """
    while True:
        schedule.run_pending()
        sleep(1)


if __name__ == '__main__':
    # Рассылка
    schedule.every().day.at("05:21").do(do_mailing)
    Thread(target=time_checker).start()

    # Запуск бота
    bot.polling()
