from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

BTN_CHATBOT = "Чат-бот"
BTN_FACT_TEXT = "Цікаві факти"
BTN_FAMOUS_PERSON = "Відома особистість"
BTN_SETTINGS = "Налаштування"


main_menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=BTN_CHATBOT),
            KeyboardButton(text=BTN_FACT_TEXT),
            KeyboardButton(text=BTN_FAMOUS_PERSON)

        ],
        [
            KeyboardButton(text=BTN_SETTINGS)
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder="Обери пункт меню"
)


famous_people = {
    "famous_person_1": "Арнольд Шварцнегер",
    "famous_person_2": "Ілон Маск",
    "famous_person_3": "Бред Піт",
}



famous_people_inline_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=name, callback_data=callback)]
        for callback, name in famous_people.items()
    ]
)

#shift + f6