import logging

from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery

import keyboards.reply as rkb
import keyboards.inline as ikb



router = Router()

@router.message(CommandStart())
async def handle_start(message:Message):
    logging.info(f"Користувач {message.from_user.id} натиснув старт")

    await message.answer(
        f"Привіт, {message.from_user.first_name}!\n"
        "Тут ти можеш поспілкуватись з відомими особистостями, пройти квіз та дізнатись випадковий факт",
        reply_markup = rkb.main_menu_kb
    )

@router.message(Command(commands=["help"]))
async def handle_help(message:Message):
    await message.answer(
        "Доступні команди: \n"
        "/start - Розпочати\n"
        "/help - Список команд\n"
        "/random - Випадковий факт\n"
        "/gpt - Чат-бот\n"
    )



@router.message(F.text == rkb.BTN_GPT)
async def handle_gpt(message:Message):
    await message.answer("CHATBOT")

@router.message(F.text == rkb.BTN_TALK)
async def handle_talk(message: Message):
    await message.answer("Обери особистість з якою ти хочеш поспілкуватись: ")

@router.message(F.text == rkb.BTN_FACT)
async def handle_fact(message:Message):
    await message.answer("Fact")

@router.message(F.text == rkb.BTN_QUIZ)
async def handle_quiz(message:Message):
    await message.answer("Quiz")



# @router.callback_query(F.data.startswith("famous_person"))
# async def handle_famous_person(callback: CallbackQuery):
#     await callback.message.answer(f"Ти натиснув {kb.famous_people[callback.data]}")
#
#     await callback.answer("Все ок!")
#



















# @router.message(F.video_note)
# async def handle_voice(message:Message):
#     await message.answer("це кружок")
#
# @router.message(F.text.lower() == "привіт")
# async def handle_text(message:Message):
#     await message.answer("і тобі привіті")
#
# @router.message(F.text)
# async def handle_text(message:Message):
#     await message.answer("це текстм ")
#
# @router.message(F.sticker)
# async def handle_stiker(message:Message):
#     await message.answer("це стікер   ")


# @router.message(F.text.startswith("/"))
# async def handler_all_commands(message:Message):
#     await message.answer(
#     f"Я не знаю команду {message.text}\n"
#     )
#
# @router.message()
# async def handler_message(message:Message):
#     await message.answer(message.text)