from aiogram import types, Dispatcher


async def set_default_commands(dispatcher: Dispatcher):
    await dispatcher.bot.set_my_commands(
        [
            types.BotCommand('start', 'Запустить бота'),
            types.BotCommand('help', 'Показать справку'),
            types.BotCommand('reset', 'Прервать операцию и выйти в основное меню')
        ]
    )
