from aiogram.types import CallbackQuery

from keyboards.inline import main_menu_keyboard
from loader import dp, bot
from utils.db.services import DbCommands


@dp.callback_query_handler(text_contains='show_history_meeting', state=None)
async def show_request_history_button(call: CallbackQuery):
    await call.answer(cache_time=10)
    await call.message.edit_reply_markup(reply_markup=None)

    meetings = await DbCommands.get_meetings_by_user(user=await DbCommands.get_user(user_id=call.from_user.id))
    if len(meetings) > 0:
        await call.message.answer('Ваши встречи:')
        for meet in meetings:
            await call.message.answer(meet.to_msg)
            if meet.location is not None:
                location = meet.get_location()
                await bot.send_location(chat_id=call.from_user.id,
                                        latitude=location['latitude'],
                                        longitude=location['longitude']
                                        )
    else:
        await call.message.answer('У Вас нет встреч.\nВыберите существующую заявку или создайте новую!')
    await call.message.answer(text='Выберите действие:', reply_markup=main_menu_keyboard)
