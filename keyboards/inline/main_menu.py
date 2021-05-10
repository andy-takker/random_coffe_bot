from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_data import action_callback

main_menu_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Создать заявку на встречу',
                                 callback_data=action_callback.new(name='create_request')),
        ],[ InlineKeyboardButton(text='Мои заявки',
                                 callback_data=action_callback.new(name='show_history_request')),
            InlineKeyboardButton(text='История встреч',
                                 callback_data=action_callback.new(name='show_history_meeting')),
        ],
        [
            InlineKeyboardButton(text='Случайный выбор',
                                 callback_data=action_callback.new(name='find_random_request')),
            InlineKeyboardButton(text='Выход', callback_data=action_callback.new(name='exit')),
        ],
    ]
)
