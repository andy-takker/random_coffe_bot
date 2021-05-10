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
    await message.answer('Привет! Я RandomDinner бот, здесь вы можете оставить заявку на встречу со случайным сотрудником вашей компании и пойти с ним на обед или на кофе, если он тоже находится в поиске, так же вы можете отказаться от встречи в любой момент.')
    await message.answer(
        'Для регистрации и создании заявки от вас потребуется лишь имя, занимаемая должность, офис в котором вы находитесь а так же информации о планируемой встрече : где и когда')
    await message.answer(f'Random Dinner это отличная возможность познакомиться с новыми людьми, узнать больше о вашей компании изнутри и просто интересно провести время')
    await message.answer('При возникновении вопросов, не обрабатываемыми ботам можете обращаться к администратору @natalenko_sergey')




@dp.message_handler(Command(commands=['reset']), state='*')
async def bot_reset(message: Message, state: FSMContext):
    await state.finish()
    user = await DbCommands.get_user(user_id=message.from_user.id)
    if user is None:
        await message.answer(f'Привет, {message.from_user.full_name}', reply_markup=registration_keyboard)
    else:
        await message.answer(f'Выберите действие!', reply_markup=main_menu_keyboard)
