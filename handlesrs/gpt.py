from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

import keyboards.reply as reply_kb
import keyboards.inline as inline_kb
from gpt import send_request_ai
from utils import load_message

router = Router()


class GptStates(StatesGroup):
    dialog = State()


@router.message(Command('gpt'))
async def handle_command_gpt(message: Message, state: FSMContext):
    await state.set_state(GptStates.dialog)
    await message.answer(load_message("gpt"))


@router.message(F.text == reply_kb.BTN_GPT)
async def handle_gpt(message: Message, state: FSMContext):
    await state.set_state(GptStates.dialog)
    await message.answer(load_message("gpt"))


@router.message(GptStates.dialog, F.text & ~F.text.startswith("/"))
async def handle_gpt_message(message: Message, state: FSMContext):
    text = await send_request_ai(message.text)
    await message.answer(text, reply_markup=inline_kb.finish_kb)