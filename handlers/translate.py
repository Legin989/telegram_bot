import logging

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.chat_action import ChatActionSender

import keyboards.reply as reply_kb
import keyboards.inline as inline_kb
from gpt import ask
from filters import USER_TEXT
from catalog import FALLBACK
from utils import load_message, load_prompt


logger = logging.getLogger(__name__)
router = Router(name="translate")


class TranslateState(StatesGroup):
	choosing_language = State()
	translating = State()


@router.message(Command("translate"))
@router.message(F.text == reply_kb.BTN_TRANSLATE)
async def handle_translate_start(message: Message, state: FSMContext):
	await state.clear()
	await state.set_state(TranslateState.choosing_language)
	await message.answer(
		text=load_message("translate")
	)

@router.message(USER_TEXT, TranslateState.choosing_language)
async def handle_language_is_corect(message: Message, state: FSMContext):
	prompt = (
		load_prompt("language")
	)
	result = await ask(prompt, message.text)
	if result is None:
		await message.answer(FALLBACK)

	if result.strip().upper() == "YES":
		await state.update_data(language=message.text)
		await state.set_state(TranslateState.translating)
		await message.answer("Чудоаво така мова/діалект існує, введіть текст а я перекладу", reply_markup=inline_kb.translate_kb)
	else:
		await message.answer("Такої мови/діалекту не існує, спробуйте ще раз", reply_markup=inline_kb.translate_kb)

@router.message(TranslateState.translating, USER_TEXT)
async def handle_translate_message(message:Message, state:FSMContext):

	data = await state.get_data()
	language = data["language"]

	prompt = load_prompt("translate").format(language=language)

	async with ChatActionSender.typing(bot=message.bot, chat_id=message.chat.id):

		text = await ask(prompt, message.text)

		if text is None:
			await message.answer(FALLBACK)
			return

		await message.answer(text, reply_markup=inline_kb.translate_kb)


@router.callback_query(F.data == inline_kb.CB_TRANSLATE_CHANGE)
async def handle_translate_change(callback: CallbackQuery, state: FSMContext):
	await state.clear()
	await state.set_state(TranslateState.choosing_language)
	await callback.message.answer(
		text=load_message("translate")
	)