from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_data import action_callback

registration_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Зарегистрироваться', callback_data=action_callback.new(name='registration'))
        ]
    ]
)


