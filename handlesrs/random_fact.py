from aiogram import Router, F
from aiogram.types import Message

import keyboards.reply as reply_kb


router = Router()


@router.message(F.text == reply_kb.BTN_FACT)
async def handle_fact(message: Message):
    await message.answer("handle_fact")