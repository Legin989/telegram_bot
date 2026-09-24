import random

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

import keyboards.reply as reply_kb
from catalog import FACT_TOPICS, FALLBACK
from gpt import ask
from keyboards.inline import random_fact_kb
from utils import load_prompt


router = Router(name="random_fact")

class RandomFactStates(StatesGroup):
    fact = State()

@router.message(Command("random"))
@router.message(F.text == reply_kb.BTN_FACT)
async def handle_fact(message: Message, state: FSMContext):
    await state.set_state(RandomFactStates.fact)
    text = await ask(
        load_prompt("random").format(topic=random.choice(FACT_TOPICS))
    )

    if text is None:
        await message.answer(FALLBACK)

    await message.answer(text, reply_markup=random_fact_kb)


@router.callback_query(RandomFactStates.fact, F.data == "random:more")
async def handle_more_fact(callback: CallbackQuery, state: FSMContext):
    text = await ask(
        load_prompt("random").format(topic=random.choice(FACT_TOPICS))
    )

    if text is None:
        await callback.message.answer(FALLBACK)

    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer(text, reply_markup=random_fact_kb)

    await callback.answer()