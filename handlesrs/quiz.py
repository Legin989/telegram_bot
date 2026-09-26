import logging
import re

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.chat_action import ChatActionSender

import keyboards.reply as reply_kb
import keyboards.inline as inline_kb
from catalog import QUIZ_TOPICS, FALLBACK
from filters import USER_TEXT
from utils import load_message, image_path, load_prompt
from gpt import ask

router = Router(name="quiz")
logger = logging.getLogger(__name__)

MAX_ASKED = 10
VERDICT_RE = re.compile(r"^\W*(НЕПРАВИЛЬНО|ПРАВИЛЬНО)\W*", re.IGNORECASE)


class QuizStates(StatesGroup):
    choosing_topic = State()
    answering = State()
    waiting_next = State()


def parse_verdict(text: str) -> tuple[bool | None, str]:
    """Розбирає відповідь судді: (правильно?, пояснення). None — формат порушено."""
    match = VERDICT_RE.match(text)

    if match is None:
        return None, text

    is_correct = match.group(1).upper() == "ПРАВИЛЬНО"
    explanation = text[match.end():].strip()

    return is_correct, explanation


async def send_question(message: Message, state: FSMContext) -> None:
    """Просить у моделі нове питання за обраною темою і чекає на відповідь."""
    data = await state.get_data()
    topic = data["topic"]
    asked = data.get("asked", [])

    prompt = (
        load_prompt("quiz_question")
        .format(
            topic=QUIZ_TOPICS[topic],
            asked="\n".join(f"- {q}" for q in asked) or "(ще не було)"
        )
    )

    async with ChatActionSender.typing(bot=message.bot, chat_id=message.chat.id):
        question = await ask(prompt)

    if question is None:
        await state.set_state(QuizStates.waiting_next)
        await message.answer(FALLBACK, reply_markup=inline_kb.quiz_result_kb)
        return

    first_line = question.splitlines()[0]
    await state.update_data(question=question, asked=[*asked, first_line][-MAX_ASKED:])
    await state.set_state(QuizStates.answering)

    await message.answer(
        f"{question}\n\n✍️ Напиши відповідь — букву або текст варіанта.",
        reply_markup=inline_kb.finish_kb
    )


@router.message(Command("quiz"))
@router.message(F.text == reply_kb.BTN_QUIZ)
async def handle_quiz(message: Message, state: FSMContext):
    logger.info("Користувач %s почав квіз", message.from_user.id)

    await state.clear()
    await state.set_state(QuizStates.choosing_topic)
    await state.set_data({"score": 0, "total": 0})

    await message.answer_photo(
        photo=FSInputFile(image_path("quiz")),
        caption=load_message("quiz"),
        reply_markup=inline_kb.quiz_topics_kb()
    )


@router.callback_query(inline_kb.QuizTopicCallback.filter())
async def handle_choose_topic(
    callback: CallbackQuery,
    callback_data: inline_kb.QuizTopicCallback,
    state: FSMContext,
):
    await callback.answer()

    topic = callback_data.topic

    if topic not in QUIZ_TOPICS:
        await callback.message.answer("Такої теми вже немає. Почни заново: /quiz")
        return

    await callback.message.edit_reply_markup(reply_markup=None)
    await state.update_data(topic=topic, asked=[])
    await callback.message.answer(f"Тема: <b>{QUIZ_TOPICS[topic]}</b>")

    await send_question(callback.message, state)


@router.message(QuizStates.answering, USER_TEXT)
async def handle_answer(message: Message, state: FSMContext):
    data = await state.get_data()

    async with ChatActionSender.typing(bot=message.bot, chat_id=message.chat.id):
        verdict = await ask(
            load_prompt("quiz_check"),
            f"Питання:\n{data['question']}\n\nВідповідь гравця: {message.text}"
        )

    if verdict is None:
        await message.answer(f"{FALLBACK}\nНадішли відповідь ще раз.")
        return

    is_correct, explanation = parse_verdict(verdict)

    if is_correct is None:
        logger.warning("Суддя порушив формат відповіді: %r", verdict)
        await state.set_state(QuizStates.waiting_next)
        await message.answer(
            f"🤔 Не вдалося оцінити відповідь, бал не нараховано.\n\n{explanation}",
            reply_markup=inline_kb.quiz_result_kb
        )
        return

    score = data.get("score", 0) + int(is_correct)
    total = data.get("total", 0) + 1

    await state.update_data(score=score, total=total)
    await state.set_state(QuizStates.waiting_next)

    header = "✅ Правильно!" if is_correct else "❌ Неправильно."
    await message.answer(
        f"{header}\n{explanation}\n\n🏆 Рахунок: <b>{score} з {total}</b>",
        reply_markup=inline_kb.quiz_result_kb
    )


@router.callback_query(inline_kb.QuizActionCallback.filter(F.action == "next"))
async def handle_next_question(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_reply_markup(reply_markup=None)

    if "topic" not in await state.get_data():
        await callback.message.answer("Квіз уже завершено. Почни заново: /quiz")
        return

    await send_question(callback.message, state)


@router.callback_query(inline_kb.QuizActionCallback.filter(F.action == "change_topic"))
async def handle_change_topic(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_reply_markup(reply_markup=None)

    await state.set_state(QuizStates.choosing_topic)
    await callback.message.answer(
        "Обери нову тему:",
        reply_markup=inline_kb.quiz_topics_kb()
    )


@router.message(QuizStates.choosing_topic, USER_TEXT)
async def handle_text_before_topic(message: Message):
    await message.answer("Спершу обери тему кнопкою вище 👆")


@router.message(QuizStates.waiting_next, USER_TEXT)
async def handle_text_after_result(message: Message):
    await message.answer(
        "Відповідь уже зараховано. Обери, що далі 👇",
        reply_markup=inline_kb.quiz_result_kb
    )