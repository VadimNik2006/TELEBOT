from aiogram import types


def search_buttons():
    buttons = [
        [
            types.InlineKeyboardButton(text="полная информация", callback_data="full_info"),
            types.InlineKeyboardButton(text="трейлеры", callback_data="trailers"),
        ]
    ]
    return buttons


def create_search_kb():
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=search_buttons())
    return keyboard
