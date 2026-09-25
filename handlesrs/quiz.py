import re

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State

import keyboards.reply as reply_kb
import keyboards.inline as inline_kb
from catalog import QUIZ_TOPICS, FALLBACK
from filter import USER_TEXT
from utils import load_message, image_path, load_prompt
from gpt import ask

router = Router(name="quiz")


MAX_ASKED = 10
VERDICT_RE = re.compile(r"^\W*(НЕПРАВИЛЬНО|ПРАВИЛЬНО)\W*$", re.IGNORECASE)


class QuizStates(StatesGroup):
    choosing_topic = State()
    answering = State()



@router.message(Command("quiz"))
@router.message(F.text == reply_kb.BTN_QUIZ)
async def handle_quiz(message: Message, state: FSMContext):
    await state.set_state(QuizStates.choosing_topic)

    await message.answer_photo(
        photo=FSInputFile(image_path("quiz")),
        text=load_message("quiz"),
        reply_markup=inline_kb.catalog_kb
    )


@router.callback_query(QuizStates.choosing_topic, F.data.startswith("quiz_"))
async def handle_choose_topic(callback: CallbackQuery, state: FSMContext):
    cb_data = callback.data.split("_")[1]

    if cb_data not in QUIZ_TOPICS:
        await callback.answer("Такої теми не існує")

    data = await state.get_data()
    asked = data.get("asked", [])

    prompt = (
        load_prompt("quiz_question")
        .format(
            topic=QUIZ_TOPICS[cb_data],
            asked="\n".join(asked)
        )
    )

    question = await ask(prompt)

    if question is None:
        await callback.message.answer(FALLBACK)

    await state.update_data(asked=[*asked, question.splitlines()[0]], question=question)

    await callback.message.answer(
        question,
        reply_markup=inline_kb.finish_kb
    )

    await state.set_state(QuizStates.answering)

    await callback.answer()

@router.message(QuizStates.answering, USER_TEXT)
async def handle_answer(message: Message, state: FSMContext):
    data = await state.get_data()

    prompt = (
        load_prompt("quiz_check"),

    )

    text = await ask(
        load_prompt("quiz_check"),
        f"Питання: {data["question"]}\n\nВідповідь: {message.text}"
    )

    if text is None:
        await message.answer(FALLBACK)


    await message.answer(text)