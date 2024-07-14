from aiogram import types


def create_start_kb():
    buttons = [
        [
            types.InlineKeyboardButton(text="список команд", callback_data="commands_list"),
            types.InlineKeyboardButton(text="поиск фильмов", callback_data="search")
        ],
        [
            types.InlineKeyboardButton(text="история", callback_data="history"),
            types.InlineKeyboardButton(text="избранные", callback_data="favorite")
        ],
        [types.InlineKeyboardButton(text="старт", callback_data="start")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


# def create_start_kb():
#     builder = InlineKeyboardBuilder()
#     builder.
#     builder.add(get_keyboard())
#     return builder.as_markup()
