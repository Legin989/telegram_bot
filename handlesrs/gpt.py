from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

import keyboards.reply as reply_kb
import keyboards.inline as inline_kb
from catalog import FALLBACK
from filter import USER_TEXT
from gpt import ask
from utils import load_message, load_prompt

router = Router(name="gpt")



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


@router.message(GptStates.dialog, USER_TEXT)
async def handle_gpt_message(message: Message, state: FSMContext):
    text = await ask(load_prompt("gpt"), message.text)

    # data = await state.get_data()
    # messages = [*data["messages"], text]
    # await state.update_data(messages=messages)

    if text is None:
        await message.answer(FALLBACK)


    if isinstance(text, list):
        for ind, text_item in enumerate(text):
            await message.answer(
                text_item,
                reply_markup=inline_kb.finish_kb if ind == len(text)-1 else None
            )

    await message.answer(text, reply_markup=inline_kb.finish_kb)