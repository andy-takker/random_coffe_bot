from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Регистрация', request_contact=True),
        ],
    ],
    resize_keyboard=True
)
