from aiogram import executor, Dispatcher
from loader import dp, bot

import middlewares
import handlers
from utils.bot_commands import set_default_commands
from utils.db import create_db
from utils.db.services import DbCommands
from utils.notify_admins import on_startup_notify


async def on_startup(dispatcher: Dispatcher):
    await set_default_commands(dispatcher)

    await on_startup_notify(dispatcher)

    await create_db()


async def on_shutdown(dispatcher: Dispatcher):
    pass


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
