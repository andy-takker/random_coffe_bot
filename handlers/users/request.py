import datetime
import logging

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from keyboards.inline import main_menu_keyboard, choosing_request_keyboard
from keyboards.inline.callback_data import choosing_datetime_callback
from keyboards.inline.choosing_time import choosing_time_keyboard, choosing_date_keyboard
from loader import dp, bot
from states.request_form import RequestForm, AcceptRequest
from utils.db.services import DbCommands


@dp.callback_query_handler(text_contains='create_request', state=None)
async def create_request_button(call: CallbackQuery):
    await call.answer(cache_time=10)
    await call.message.edit_reply_markup(reply_markup=None)

    await call.message.answer("Введите цель встречи:")
    await RequestForm.first()


@dp.message_handler(state=RequestForm.purpose_q)
async def answer_purpose(message: Message, state: FSMContext):
    answer = message.text
    async with state.proxy() as data:
        data['purpose'] = answer
    await message.answer(f'Введите место встречи:\n(Вы можете отправить геолокацию)')
    await RequestForm.next()


@dp.message_handler(state=RequestForm.place_q, content_types=['location', 'text'])
async def answer_place(message: Message, state: FSMContext):
    if message.text is not None:
        async with state.proxy() as data:
            data['place'] = message.text
            data['location'] = None
    elif message.location is not None:
        async with state.proxy() as data:
            data['location'] = {'longitude': message.location.longitude, 'latitude': message.location.latitude}
            data['place'] = None
    await message.answer(f'Введите дату и время в формате\n(в формате ДД-ММ-ГГГГ ЧЧ:ММ)',
                         reply_markup=choosing_time_keyboard)
    await RequestForm.next()


def is_date(str_date: str) -> bool:
    try:
        a = datetime.datetime.strptime(str_date, '%d-%m-%Y %H:%M')
        now = datetime.datetime.now()
        if a < now:
            return False
        else:
            return True
    except ValueError:
        return False


@dp.message_handler(lambda message: not is_date(message.text), state=RequestForm.date_q)
async def answer_date_invalid(message: Message):
    return await message.reply('Введите правильную дату!')


@dp.message_handler(state=RequestForm.date_q)
async def answer_message_date(message: Message, state: FSMContext):
    answer = message.text
    async with state.proxy() as data:
        data['date'] = datetime.datetime.strptime(answer, '%d-%m-%Y %H:%M')
    await message.answer(f'Почти все...\nЕсли хотите, оставьте комментарий или пожелание для собеседника:')
    await RequestForm.next()


@dp.callback_query_handler(choosing_datetime_callback.filter(datetime='time'), state=RequestForm.date_q)
async def answer_callback_time(call: CallbackQuery, callback_data: dict, state: FSMContext, ):
    await call.answer(cache_time=5)
    await call.message.edit_reply_markup(reply_markup=None)
    async with state.proxy() as data:
        dt = datetime.datetime.now().replace(hour=int(callback_data['hour']), minute=int(callback_data['minute']))
        data['date'] = dt
    await call.message.answer(f'Выберите день:', reply_markup=choosing_date_keyboard)


@dp.callback_query_handler(choosing_datetime_callback.filter(datetime='date'), state=RequestForm.date_q)
async def answer_callback_time(call: CallbackQuery, callback_data: dict, state: FSMContext, ):
    await call.answer(cache_time=5)
    await call.message.edit_reply_markup(reply_markup=None)
    async with state.proxy() as data:
        dt = data['date']
        data['date'] = dt.replace(day=int(callback_data['day']), month=int(callback_data['month']), year=int(callback_data['year']))
    await call.message.answer(f'Почти все...\nЕсли хотите, оставьте комментарий или пожелание для собеседника:')
    await RequestForm.next()


@dp.message_handler(state=RequestForm.comment_q)
async def answer_comment(message: Message, state: FSMContext):
    answer = message.text
    async with state.proxy() as data:
        data['comment'] = answer
        request = await DbCommands.create_request(user_id=message.from_user.id, data=data)
        await message.answer('Заявка успешно создана')
        await state.finish()
        await message.answer(request.to_msg, reply_markup=main_menu_keyboard)
        if request.location is not None:
            location = request.get_location()
            await bot.send_location(
                chat_id=message.from_user.id,
                longitude=location['longitude'],
                latitude=location['latitude'], )


@dp.callback_query_handler(text_contains='show_history_request', state=None)
async def show_request_history_button(call: CallbackQuery):
    await call.answer(cache_time=10)
    await call.message.edit_reply_markup(reply_markup=None)

    requests = await DbCommands.get_requests_by_user(user=await DbCommands.get_user(user_id=call.from_user.id))
    if len(requests) > 0:
        await call.message.answer('Ваши заявки:')
        for req in requests:
            await call.message.answer(req.to_msg)
            if req.location is not None:
                location = req.get_location()
                await bot.send_location(
                    chat_id=call.from_user.id,
                    longitude=location['longitude'],
                    latitude=location['latitude'], )
    else:
        await call.message.answer('У Вас нет активных заявок')
    await call.message.answer(text='Выберите действие:', reply_markup=main_menu_keyboard)


@dp.callback_query_handler(text_contains='find_random_request', state="*")
async def find_random_request_button(call: CallbackQuery):
    await call.answer(cache_time=2)
    await call.message.edit_reply_markup(reply_markup=None)
    request = await DbCommands.get_random_request(user=await DbCommands.get_user(user_id=call.from_user.id))
    if request is not None:
        await call.message.answer(text=request.to_msg, reply_markup=choosing_request_keyboard)
        if request.location is not None:
            location = request.get_location()
            await bot.send_location(
                chat_id=call.from_user.id,
                longitude=location['longitude'],
                latitude=location['latitude'], )
        await AcceptRequest.first()
        state = dp.get_current().current_state()
        await state.update_data(request_id=request.id)
    else:
        await call.message.answer('К сожалению сейчас нет свободных заявок', reply_markup=main_menu_keyboard)


@dp.callback_query_handler(text_contains='accept_request', state=AcceptRequest.accept)
async def accept_request_button(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=5)
    await call.message.edit_reply_markup(reply_markup=None)
    async with state.proxy() as data:
        request_id = data['request_id']
        meeting_id = await DbCommands.create_meeting_from_request(request_id=request_id, user_id=call.from_user.id)
    await state.finish()
    meeting = await DbCommands.get_meeting(meeting_id=meeting_id)
    await call.message.answer(text=meeting.to_msg, reply_markup=main_menu_keyboard)
    await bot.send_message(chat_id=meeting.request_user.user_id, text="Вашу заявку приняли!")
    await bot.send_message(chat_id=meeting.request_user.user_id, text=meeting.to_msg, reply_markup=main_menu_keyboard)
    if meeting.location is not None:
        location = meeting.get_location()
        await bot.send_location(
            chat_id=call.from_user.id,
            latitude=location['latitude'],
            longitude=location['longitude'],
        )


@dp.callback_query_handler(text_contains='to_main_menu', state='*')
async def exit_to_main_menu_button(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.answer(cache_time=10)
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer(text='Выберите действие:', reply_markup=main_menu_keyboard)


@dp.callback_query_handler(text_contains='exit', state='*')
async def exit_button(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.answer(cache_time=10)
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer('До свидания!')
