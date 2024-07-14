from aiogram import types


def create_search_kb():
    buttons = [
        [
            types.InlineKeyboardButton(text="получить полную информацию о фильме", callback_data="full_info"),
        ],
        [
            types.InlineKeyboardButton(text="получить трейлеры фильма", callback_data="trailers"),
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
