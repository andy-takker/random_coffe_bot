from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_data import action_callback

choosing_request_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Принять',
                                 callback_data=action_callback.new(name='accept_request')),
            InlineKeyboardButton(text='Найти другую',
                                 callback_data=action_callback.new(name='find_random_request')),
            InlineKeyboardButton(text='Выход',
                                 callback_data=action_callback.new(name='to_main_menu'))
        ],
    ]
)
