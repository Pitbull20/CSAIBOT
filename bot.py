import telebot
import datetime

from DataBase.db import DataBase
from config import config

schedule = {
    "Monday": {
        "not_even": "9:35, каб. 6308: Системне програмування та архітектура комп'ютерів, викладач Осолінський Олександр Романович\n11:10, каб. 6308: Вища математика, викладач Алілуйко Андрій Миколайович\n12:50, каб. 6308: Фізика, викладач Паздрій Ігор Ростиславович",
        "pair": "9:35, каб. 6308: Системне програмування та архітектура комп'ютерів, викладач Осолінський Олександр Романович\n11:10, каб. 6308: Вища математика, викладач Алілуйко Андрій Миколайович\n12:50, каб. 6308: Фізика, викладач Паздрій Ігор Ростиславович"
    },
    "Tuesday": {
        "not_even": "8:00, каб. 6104: Сучасні парадигми програмування, викладач Биковий Павло Євгенович\n9:35, каб. 6104: Дискретна математика, викладачка Мартинюк Олеся Миронівна",
        "pair": "8:00, каб. 6104: Сучасні парадигми програмування, викладач Биковий Павло Євгенович\n9:35, каб. 6104: Дискретна математика, викладачка Мартинюк Олеся Миронівна\n12:50, актовий зал (1 корпус): Політологія, викладач Томахів Володимир Ярославович"
    },
    "Wednesday": {
        "not_even": "9:35, каб. 6303: Системне програмування та архітектура комп'ютерів, викладач Кіт Іван Романович\n11:10, каб. 6301: Вища математика, викладач Алілуйко Андрій Миколайович\n12:50, каб. 6302: Фізика, викладач Дериш Богдан Богданович",
        "pair": "11:10, каб. 6301: Вища математика, викладач Алілуйко Андрій Миколайович\n12:50, каб. 6302: Фізика, викладач Дериш Богдан Богданович"
    },
    "Thursday": {
        "not_even": "12:50, каб. 5508: Іноземна мова, викладачка Штохман Лілія Миколаївна\n14:25, каб. 5509: Сучасні парадигми програмування, викладач Кіт Іван Романович",
        "pair": "11:10, каб. 5506: Політологія, викладач Томахів Володимир Ярославович\n12:50, каб. 5508: Іноземна мова, викладачка Штохман Лілія Миколаївна\n14:25, каб. 5509: Сучасні парадигми програмування, викладач Кіт Іван Романович"
    },
    "Friday": {
        "not_even": "12:50, каб. 5505: Дискретна математика, викладачка Мартинюк Олеся Миронівна\n14:25, каб. 5501: Системне програмування та архітектура комп'ютерів, Викладач: Кіт Іван Романович",
        "pair": "12:50, каб. 5505: Дискретна математика, викладачка Мартинюк Олеся Миронівна\n14:25, каб. 5501: Системне програмування та архітектура комп'ютерів, Викладач: Кіт Іван Романович"
    },
}


def is_week_even(date_string):
    date = datetime.datetime.strptime(date_string, '%d.%m.%Y')
    week_number = date.isocalendar()[1]
    if week_number % 2 == 0:
        return 2
    else:
        return 1


# створюємо екземпляр бота з токеном, який отримано від BotFather
bot = telebot.TeleBot(config['TOKEN'])


# функція, яка обробляє повідомлення з текстом дати

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привіт :)\nЦей бот завжди підкаже тобі які в тебе пари\nПросто введи дату у форматі 'дд.мм'")


def get_day_of_week(date, message):
    try:
        # конвертуємо текст повідомлення в об'єкт дати
        date_obj = datetime.datetime.strptime(f"{date}.2023", '%d.%m.%Y')
        # отримуємо день тижня з об'єкту дати та відправляємо його користувачу
        day_of_week = date_obj.strftime('%A')
        if is_week_even(f"{date}.2023") == 2:
            if day_of_week == 'Saturday' or day_of_week == 'Sunday':
                bot.reply_to(message, "Сьогодні вихідний, можеш балдіти :)")
                return
            else:
                bot.reply_to(message, schedule[day_of_week]["pair"])
        else:
            if day_of_week == 'Saturday' or day_of_week == 'Sunday':
                bot.reply_to(message, "Сьогодні вихідний, можеш балдіти :)")
                return
            bot.reply_to(message, schedule[day_of_week]["not_even"])
    except ValueError:
        bot.reply_to(message, "Неправильний формат дати! Введіть дату у форматі 'дд.мм'")


def is_user_admin(message, bot):
    for u in bot.get_chat_administrators(message.chat.id):
        if message.from_user.id == u.user.id:
            return True
    return False


@bot.message_handler(commands=['get'])
def get(message):
    date = message.text.split(" ")
    get_day_of_week(date[1], message)


# @bot.message_handler(commands=['setgroup'])
# def setgroup(message):
#     if is_user_admin(message, bot):
#         db = DataBase("DataBase.db")
#         db.create(int(message.chat.id))
#         db.get_all_elements()


# запускаємо бота
print("Bot was started")
bot.polling()
