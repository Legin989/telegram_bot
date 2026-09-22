import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand

from config import settings
from handlesrs import routers


logger = logging.getLogger(__name__)


async def set_commands(bot: Bot) -> None:
    await bot.set_my_commands([
        BotCommand(command="start",description="Почати"),
        BotCommand(command="help", description="Допомога"),
        BotCommand(command="random", description="Випадковий факт"),
        BotCommand(command="gpt", description="Питання до Chat-GPT"),
    ])


def setup_logging() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    logging.basicConfig(
        level=logging.INFO,
        stream=sys.stdout,
        format="[%(asctime)s - %(name)s - %(levelname)s - %(message)s]"
    )
    logging.getLogger('aiogram:').setLevel(logging.WARNING)

async def main():
    setup_logging()

    bot = Bot(
        settings.BOT_API_KEY,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    await set_commands(bot)

    dp.include_routers(routers)

    print("запускаємо бота...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Зупинка бота")