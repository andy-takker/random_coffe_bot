from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from keyboards.inline import main_menu_keyboard
import logging

from keyboards.inline.callback_data import workplace_callback
from keyboards.inline.choosing_workplace import choosing_workplace_keyboard
from loader import dp
from states.registrationform import RegistrationForm
from utils.db.services import DbCommands


@dp.callback_query_handler(text_contains='registration', state=None)
async def registration_button(call: CallbackQuery):
    await call.answer(cache_time=10)
    user = await DbCommands.get_user(user_id=call.from_user.id)
    await call.message.edit_reply_markup(reply_markup=None)
    if user is not None and user.is_registration_completed:
        await call.message.answer('Вы уже зарегистрированы', reply_markup=main_menu_keyboard, )
    else:
        if user is None:
            await DbCommands.create_user(
                user_id=call.from_user.id,
                first_name=call.from_user.first_name if call.from_user.first_name is not None else "",
                last_name=call.from_user.last_name if call.from_user.last_name is not None else "",
                username=call.from_user.username,
            )
        else:
            await call.message.answer(f'Вы не завершили регистрацию')
        await call.message.answer(f'Введите Ваше имя:\n(если хотите оставить {call.from_user.first_name}, отправьте 0)')
        await RegistrationForm.first_name_q.set()


@dp.message_handler(state=RegistrationForm.first_name_q)
async def answer_first_name(message: Message, state: FSMContext):
    answer = message.text
    async with state.proxy() as data:
        if answer != '0':
            data['first_name'] = answer
        else:
            data['first_name'] = message.from_user.first_name
    await message.answer(
        f'Введите Вашу фамилию:\n(если хотите оставить {message.from_user.last_name if message.from_user.last_name is not None else ""}, отправьте 0)')
    await RegistrationForm.next()


@dp.message_handler(state=RegistrationForm.last_name_q)
async def answer_last_name(message: Message, state: FSMContext):
    answer = message.text
    async with state.proxy() as data:
        if answer != '0':
            data['last_name'] = answer
        else:
            data['last_name'] = message.from_user.last_name if message.from_user.last_name is not None else ""
    await message.answer(f'Введите Вашу должность:')
    await RegistrationForm.next()


@dp.message_handler(state=RegistrationForm.position_q)
async def answer_position(message: Message, state: FSMContext):
    answer = message.text
    position = await DbCommands.get_position(name=answer)
    if position is None:
        position = await DbCommands.create_position(name=answer)
    async with state.proxy() as data:
        data['position_id'] = position.id
    await message.answer(f'Введите Ваше место работы:\n(выберите город, или введите текстом)',
                         reply_markup=choosing_workplace_keyboard)
    await RegistrationForm.next()


@dp.callback_query_handler(workplace_callback.filter(), state=RegistrationForm.workplace_q)
async def create_request_button(call: CallbackQuery, callback_data: dict, state: FSMContext, ):
    await call.answer(cache_time=10)
    await call.message.edit_reply_markup(reply_markup=None)
    workplace = await DbCommands.get_workplace(name=callback_data['city'])
    if workplace is None:
        workplace = await DbCommands.create_workplace(name=callback_data['city'])
    async with state.proxy() as data:
        data['workplace_id'] = workplace.id
        await DbCommands.update_user(user_id=call.from_user.id, data=data)
    await state.finish()
    await call.message.answer(f'Спасибо регистрация прошла успешно', reply_markup=main_menu_keyboard)


@dp.message_handler(state=RegistrationForm.workplace_q)
async def answer_workplace(message: Message, state: FSMContext):
    answer = message.text
    workplace = await DbCommands.get_workplace(name=answer)
    if workplace is None:
        workplace = await DbCommands.create_workplace(name=answer)
    async with state.proxy() as data:
        data['workplace_id'] = workplace.id
        await DbCommands.update_user(user_id=message.from_user.id, data=data)

    await state.finish()
    await message.answer(f'Спасибо регистрация прошла успешно', reply_markup=main_menu_keyboard)
