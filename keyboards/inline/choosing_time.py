import datetime

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_data import choosing_datetime_callback

choosing_time_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=f'{12 + i}:00', callback_data=choosing_datetime_callback.new(
                datetime='time', hour=12 + i, minute=0, year=0, month=0, day=0)),
            InlineKeyboardButton(text=f'{12 + i}:30', callback_data=choosing_datetime_callback.new(
                datetime='time', hour=12 + i, minute=30, year=0, month=0, day=0)),
        ] for i in range(6)
    ]
)
now = datetime.datetime.now()
# choosing_date_keyboard = InlineKeyboardMarkup(
#     inline_keyboard=[
#         [
#             InlineKeyboardButton(text=f'{(now + datetime.timedelta(days=2 * i)).strftime("%d.%m.%Y")}',
#                                  callback_data=choosing_datetime_callback.new(
#                                      datetime='date', hour=0, minute=0, year=0, month=0, day=0)),
#             InlineKeyboardButton(text=f'{(now + datetime.timedelta(days=2 * i + 1)).strftime("%d.%m.%Y")}',
#                                  callback_data=choosing_datetime_callback.new(
#                                      datetime='date', hour=0, minute=0, year=0, month=0, day=0)),
#         ] for i in range(7)
#     ]
# )
choosing_date_keyboard = InlineKeyboardMarkup(row_width=2)
for i in range(7):
    f = now + datetime.timedelta(days=2 * i)
    s = now + datetime.timedelta(days=2 * i + 1)
    choosing_date_keyboard.insert(
        InlineKeyboardButton(text=f'{f.strftime("%d.%m.%Y")}', callback_data=choosing_datetime_callback.new(
            datetime='date', hour=0, minute=0, year=f.year, month=f.month, day=f.day)))
    choosing_date_keyboard.insert(
        InlineKeyboardButton(text=f'{s.strftime("%d.%m.%Y")}', callback_data=choosing_datetime_callback.new(
            datetime='date', hour=0, minute=0, year=s.year, month=s.month, day=s.day)))
