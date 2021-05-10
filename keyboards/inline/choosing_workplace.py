from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_data import workplace_callback

choosing_workplace_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Санкт-Петербург', callback_data=workplace_callback.new(city='Санкт-Петербург')),
        InlineKeyboardButton(text='Тюмень', callback_data=workplace_callback.new(city='Тюмень')),
    ]
])
