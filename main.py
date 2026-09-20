import asyncio
import logging

import sys

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand

from config import settings
from handlers import router



async def set_commands(bot: Bot) -> None:
    await bot.set_my_commands([
        BotCommand(command="start",description="Почати"),
        BotCommand(command="help", description="Допомога"),
        BotCommand(command="random", description="Випадковий факт"),
        BotCommand(command="gpt", description="Чат-бот"),
    ])


async def main():
    logging.basicConfig(
        level=logging.INFO,
        stream=sys.stdout,
        encoding="utf-8",
        format="[%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    bot = Bot(settings.BOT_API_KEY)
    dp = Dispatcher()


    #command menu
    await set_commands(bot)


    dp.include_routers(router)


    print("запускаємо бота...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Зупинка бота")