from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from catalog import QUIZ_TOPICS


CB_RANDOM_MORE = "random:more"
CB_FINISH = "common:finish"

random_fact_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🔄 Хочу ще факт", callback_data=CB_RANDOM_MORE)],
        [InlineKeyboardButton(text="❌ Закінчити", callback_data=CB_FINISH)],
    ]
)

finish_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="❌ Закінчити", callback_data=CB_FINISH)],
    ]
)


catalog_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=value, callback_data=f"quiz_{cb_data}")]
        for cb_data, value in QUIZ_TOPICS.items()
    ]
)