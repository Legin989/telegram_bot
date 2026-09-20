from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

CB_RANDOM_MORE = "random:more"
CB_FINISH = "common:finish"


random_fact_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Хочу ще факт", callback_data=CB_RANDOM_MORE)],
        [InlineKeyboardButton(text="Закінчити", callback_data=CB_FINISH)]
    ]
)

finish_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Закінчити", callback_data=CB_FINISH)]
    ]
)