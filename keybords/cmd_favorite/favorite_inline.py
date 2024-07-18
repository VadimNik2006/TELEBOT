from aiogram import types


def favorite_buttons(is_liked=False):
    text = "♡" if not is_liked else "❤️"
    buttons = [
        [
            types.InlineKeyboardButton(text=text, callback_data="like")
        ]
    ]
    return buttons


def create_favorite_kb():
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=favorite_buttons())
    return keyboard
