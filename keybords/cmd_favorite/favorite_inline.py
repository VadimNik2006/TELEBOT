from aiogram import types
from aiogram.filters.callback_data import CallbackData


class LikeCallback(CallbackData, prefix="like"):
    is_search: bool
    is_liked: bool
    id_info: int


def favorite_buttons(is_search: bool = False, is_liked: bool = False, id: int = None):
    text = "♡" if not is_liked else "❤️"
    buttons = [
        [
            types.InlineKeyboardButton(text=text,
                                       callback_data=LikeCallback(is_search=is_search, is_liked=is_liked, id_info=id).pack())
        ]
    ]
    return buttons


def create_favorite_kb(is_liked=False):
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=favorite_buttons(is_liked))
    return keyboard
