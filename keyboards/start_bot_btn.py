from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start_button_user = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Написать админу"),
            KeyboardButton(text="Узнать расписание")
        ],
    ],
    resize_keyboard=True)

start_button_admin = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Спросить в чате"),
            KeyboardButton(text="Отправить расписание"),
            KeyboardButton(text="Создать опрос")
        ],
    ],
    resize_keyboard=True)



