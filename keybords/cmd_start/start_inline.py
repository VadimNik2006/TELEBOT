from aiogram import types
from aiogram.filters.callback_data import CallbackData


class MenuCallback(CallbackData, prefix='menu'):
    section: str


def create_start_kb():
    buttons = [
        [
            types.InlineKeyboardButton(text="список команд",
                                       callback_data=MenuCallback(section="commands_list").pack()),
            types.InlineKeyboardButton(text="поиск фильмов", callback_data=MenuCallback(section="search").pack())
        ],
        [
            types.InlineKeyboardButton(text="история", callback_data=MenuCallback(section="history").pack()),
            types.InlineKeyboardButton(text="избранные", callback_data=MenuCallback(section="favorite").pack())]
        # ],
        # [types.InlineKeyboardButton(text="старт", callback_data="start")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

# def create_start_kb():
#     builder = InlineKeyboardBuilder()
#     builder.
#     builder.add(get_keyboard())
#     return builder.as_markup()
