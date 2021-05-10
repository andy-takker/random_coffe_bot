from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart, CommandHelp, Command
from aiogram.types import CallbackQuery, Message

from keyboards.inline import registration_keyboard, main_menu_keyboard
from loader import dp
from utils.db.services import DbCommands
import logging


@dp.message_handler(CommandStart())
async def bot_start(message: Message):
    user = await DbCommands.get_user(user_id=message.from_user.id)
    if user is None:
        await message.answer(f'Привет, {message.from_user.full_name}', reply_markup=registration_keyboard)
    else:
        await message.answer(f'С возвращением!', reply_markup=main_menu_keyboard)


@dp.message_handler(CommandHelp())
async def bot_help(message: Message):
    user = await DbCommands.get_user(user_id=message.from_user.id)
    logging.info(message.from_user.username)
    if user is not None:
        await message.answer(f"User: {user.name} {message.from_user.username}")
    else:
        await message.answer("Вы не найдены в базе :(")


@dp.message_handler(Command(commands=['reset']), state='*')
async def bot_reset(message: Message, state: FSMContext):
    await state.finish()
    await message.answer(f'Выберите действие:', reply_markup=main_menu_keyboard)
