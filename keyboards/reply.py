from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

BTN_GPT = "Чат-бот"
BTN_FACT = "Цікаві факти"
BTN_TALK = "обистість"
BTN_QUIZ = "Квіз"


MENU_BUTTONS = {BTN_QUIZ, BTN_TALK, BTN_FACT, BTN_GPT}

main_menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=BTN_GPT)],
        [KeyboardButton(text=BTN_FACT)],
        [KeyboardButton(text=BTN_TALK)],
        [KeyboardButton(text=BTN_QUIZ)],
    ],
    resize_keyboard=True,
    input_field_placeholder="Обери пункт меню"
)
