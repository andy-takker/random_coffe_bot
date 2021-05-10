from aiogram.utils.callback_data import CallbackData

action_callback = CallbackData('action', 'name')
choosing_datetime_callback = CallbackData('choosing_datetime', 'datetime', 'hour', 'minute', 'year', 'month', 'day')

workplace_callback = CallbackData('workplace', 'city')