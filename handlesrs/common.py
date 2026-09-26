import logging
from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile, Message, CallbackQuery

import keyboards.reply as reply_kb
import keyboards.inline as inline_kb
from utils import image_path, load_message


router = Router(name="common")
logger = logging.getLogger(__name__)



async def show_main_menu(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer_photo(
        photo=FSInputFile(image_path("main")),
        caption=load_message("main"),
        reply_markup=reply_kb.main_menu_kb,
    )


@router.message(CommandStart())
async def handle_start(message: Message, state: FSMContext):
    logger.info("Користувач %s натиснув /start", message.from_user.id)

    await show_main_menu(message, state)


@router.message(Command(commands=["help"]))
async def handle_help(message: Message):
    await message.answer(
        "Доступні команди:\n"
        "/start - Розпочати\n"
        "/help - Ця команда\n"
        "/random - Випадковий факт\n"
        "/gpt - Чат-бот\n"
        "/talk - Діалог з відомою особистістю\n"
        "/quiz - Квіз\т"
        "/recommend - Рекомендації"
    )


@router.callback_query(F.data == inline_kb.CB_FINISH)
async def handle_finish(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await callback.message.edit_reply_markup(reply_markup=None)
    await show_main_menu(callback.message, state)